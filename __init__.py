from flask import Flask, render_template, request, redirect, flash, url_for, session
from mysql_dbconnect import *
from pymysql import escape_string as thwart
from bokeh.embed import components
from graphs import *
from secret_hash import *
from functools import wraps
import customjsonfunc
import gc
import os
import json


#Creating the Flask app.
app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.route('/admin/temp/')
def admin_temp():
    return render_template("temp.html")


@app.route('/admin/dashboard/analysis/displaygraph/', methods = ['POST'])
def display_graph():
    bargraph_obj = call_bar_graph()
    bargraph_div, bargraph_script = components(bargraph_obj)

    timeline_obj = call_year_graph()
    timeline_div, timeline_script = components(timeline_obj)

    return render_template('display_graph.html', bargraph_div = bargraph_div, bargraph_script = bargraph_script, timeline_div = timeline_div, timeline_script = timeline_script)


#Created a login_required wrapper function that wraps other functions in-order to force to do login first before accessing any pages.
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('admin_login'))
    return wrap

#Route and function for about functionality.
@app.route('/admin/about/', methods = ['GET', 'POST'])
def admin_about():
    return render_template("about.html")

#Route and function for logs functionality.
@app.route('/admin/logs/', methods = ['GET', 'POST'])
def admin_logs():
    return render_template("logs.html")

#Route and function for schedule success functionality.
@app.route('/admin/schedule/done/', methods = ['GET', 'POST'])
def admin_schedule_success():
    if request.method == "POST":
        try:
            err = "Email sending has been started. Thankyou."
            return render_template("schedulesuccess.html", err=err)
        except Exception as e:
            return render_template("schedulesuccess.html", err=str(e))

#Route and function for schedule functionality.
@app.route('/admin/schedule/', methods = ['GET', 'POST'])
def admin_schedule():
    SEMESTER_LIST = ["8", "7", "6", "5", "4", "3", "2", "1"]
    FORMS_LIST = customjsonfunc.list_out_forms()
    return render_template("schedule.html", SEMESTER_LIST=SEMESTER_LIST, FORMS_LIST=FORMS_LIST)

#Route and function for analysis show report functionality. A next page for analysis.html
@app.route('/admin/analysis/showreport/', methods = ['GET', 'POST'])
def admin_analysis_showreport():
    if request.method == "POST":
        try:
            err = ""
            faculty_name = request.form['faculty_name']
            semester = request.form.getlist('semester')

            c, conn = connect_to("pumis")
            c.execute("SELECT post, dept, institute, email, id, avatar FROM faculty_new WHERE full_name=(%s)", (faculty_name))

            x = c.fetchone()

            c.close()
            conn.close()
            gc.collect()

            post = x[0]
            dept = x[1]
            institute = x[2]
            email = x[3]
            id = x[4]
            avatar = x[5]

            dept = dept + " Department"
            img_file_link = "static/images/facuties/" + avatar
            faculty_mailto_email = "mailto:" + str(email)
            return render_template("showreport.html", err=err, faculty_name=faculty_name, img_file_link=img_file_link, faculty_mailto_email=faculty_mailto_email, post=post, dept=dept, institute=institute, id=id)

        except Exception as e:
            return render_template("showreport.html", err=str(e), faculty_name=faculty_name, img_file_link=img_file_link, faculty_mailto_email=faculty_mailto_email, post=post, dept=dept, institute=institute, id=id)



#Route and function for analysis functionality.
@app.route('/admin/analysis/', methods = ['GET', 'POST'])
def admin_analysis():
    c, conn = connect_to("pumis")
    c.execute("SELECT first_name, last_name FROM faculty GROUP BY first_name, last_name")
    data = c.fetchall()
    c.close()
    conn.close()
    gc.collect()
    full_name_list = list()
    for i in data:
        full_name_list.append(i[0] + " " + i[1])

    return render_template('analysis.html', full_name_list=full_name_list)


#Route and function for create form success functionality.
@app.route('/admin/createform/success/', methods=["GET", "POST"])
def admin_createform_success():
    try:
        err = ""
        if request.method == "POST":
            FORMS_LIST_count = customjsonfunc.count_forms()
            form_name = request.form['form_name']
            new_quest_list = list()
            for i in range(1, 11):
                new_quest_list.append(str(request.form["new_quest_" + str(i)]))

            if customjsonfunc.jsonifyforms(form_name, new_quest_list) is True:
                err = "Your form is successfully saved and FPSU ChatBot has started learning from it!"
            else:
                err = "Somthing went wrong. Try again."

        return render_template("createform_success.html", err=err, FORMS_LIST_count=FORMS_LIST_count)

    except Exception as e:
        return render_template("createform_success.html", err=str(e), FORMS_LIST_count=FORMS_LIST_count)


#Route and function for create form functionality.
@app.route('/admin/createform/')
def admin_createform():
    FORMS_LIST = customjsonfunc.list_out_forms()
    FORMS_LIST_count = customjsonfunc.count_forms()
    return render_template("createform.html", FORMS_LIST=FORMS_LIST, FORMS_LIST_count=FORMS_LIST_count)

#Route and function for log out.
@app.route('/admin/logout/')
@login_required
def admin_logout():
    err = "You have been successfully logged out."
    session.clear()
    gc.collect()
    return render_template("login.html", err=err)


#Route and function for admin dashboard.
@app.route("/admin/dashboard/", methods=["GET", "POST"])
@login_required #login_required wrapper created above is used here. It should be always placed under the main Flask app wrapper.
def admin_dashboard():
    return render_template("dashboard.html")

#Route and function for admin login.
@app.route("/admin/login/", methods=["GET", "POST"])
def admin_login():
    err="" #Defining err a login page jinja variable.
    try:
        #Authenticating username and password with database.
        c, conn = connect_to("fpsu")
        if request.method=="POST":
            username = request.form['username']
            c.execute("SELECT password FROM user WHERE email = (%s)", (username))
            password_stored = c.fetchone()[0]
            password = request.form['password']
            if password == password_stored:
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('admin_dashboard')) #Redirect to admin dashboard page if login is successful.
            else:
                err = "Invalid Credentials. Please try again!" #Error message defined.

        return render_template("login.html", err=err) #Returning login page again in case of above authentication fails, alongwith err in jinja variable names err.
    except Exception as e:
        return render_template("login.html", err=str(e)) #DEBUG PURPOSE : Exception Handling with passing exception message into jinja varialbe err.


@app.route('/feedback_desc_part1/')
def feedback_desc_part1():
    try:
        return render_template('feedback_desc_part1.html')
    except Exception as e:
        return str(e)

@app.route('/feedback_desc_part2/')
def feedback_desc_part2():
    try:
        return render_template('feedback_desc_part2.html')
    except Exception as e:
        return str(e)


@app.route('/feedback_desc_part1_resp/', methods=['GET', 'POST'])
def feedback_desc_part1_resp():
    try:
        qresp_list = list()
        for i in range(1,6):
            qresp_list.append(str(request.form['quest_' + str(i)]))

        c, conn = connection_to_datahouse()
        c.execute("INSERT INTO fdbck_resp_training VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (qresp_list[0], qresp_list[1], qresp_list[2],
        qresp_list[3], qresp_list[4], "", "", "", "", ""))

        conn.commit()
        c.close()
        conn.close()
        gc.collect()
        response_msg = "Thanks. Your response is recorded."
        return render_template('feedback_desc_resp.html', response_msg = response_msg)
    except Exception as e:
        response_msg= "A record with your enrollment number already exists. You cannot fill in more."
        return render_template('feedback_desc_resp.html', response_msg = response_msg + "\n" + str(e) )

@app.route('/feedback_desc_part2_resp/', methods=['GET', 'POST'])
def feedback_desc_part2_resp():
    try:
        qresp_list = list()
        for i in range(6,11):
            qresp_list.append(str(request.form['quest_' + str(i)]))

        c, conn = connection_to_datahouse()
        c.execute("INSERT INTO fdbck_resp_training VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ( "", "", "", "", "", qresp_list[0], qresp_list[1], qresp_list[2],
        qresp_list[3], qresp_list[4]))

        conn.commit()
        c.close()
        conn.close()
        gc.collect()
        response_msg = "Thanks. Your response is recorded."
        return render_template('feedback_desc_resp.html', response_msg = response_msg)
    except Exception as e:
        response_msg= "A record with your enrollment number already exists. You cannot fill in more."
        return render_template('feedback_desc_resp.html', response_msg = response_msg + "\n" + str(e) )

# For registering student details for the system
@app.route('/register/')
def register():
    return render_template('register.html')

#Ack route and page for above defined function.
@app.route('/registered/', methods = ['POST'])
def registered():
    enrollment_number = int(request.form['enrollment_number'])
    first_name = str(request.form['first_name'])
    last_name = str(request.form['last_name'])
    institute_name = str(request.form['institute_name'])
    department_name = str(request.form['department_name'])
    semester = str(request.form['semester'])
    student_class = str(request.form['class'])
    email_id = str(request.form['email'])
    mobile_phone_number = int(request.form['mobile_phone_number'])

    c, conn = connection_to_pumis()
    c.execute("INSERT INTO student VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (enrollment_number, first_name, last_name, institute_name, department_name, semester, student_class, email_id, mobile_phone_number))
    conn.commit()
    c.close()
    conn.close()
    gc.collect()

    return render_template('registered.html')


@app.route('/student_table_resp/')
def student_table_resp():
    c, conn = connection_to_pumis()
    c.execute("SELECT first_name, last_name, mobile_number FROM student")
    response_data = c.fetchall()
    count = 0
    for x in response_data:
        count += 1

    return render_template('student_table_resp.html', student_table_response = response_data, total_count = count)

@app.route('/resp/', methods = ['POST'])
def resp():
    ques_1_resp = request.form['ques_1_resp'] # Yes = 1, No = 0
    ques_2_resp = request.form['ques_2_resp'] # Yes = 1, No = 0
    ques_3_resp = request.form['ques_3_resp'] # Yes = 1, No = 0
    ques_4_resp = request.form['ques_4_resp'] # Yes = 1, No = 0
    ques_5_resp = request.form['ques_5_resp'] # Black Board = 1, Projector Aided = 0
    return render_template('resp.html')

@app.route('/chatbot/<unique_route_string>', methods=['GET'])
def chatbot_page(unique_route_string):
    try:
        c, conn = connect_to()
        c.execute("SELECT enrollment_number FROM fpsu.route_string WHERE string=%s", (unique_route_string))
        enrollment_number = (c.fetchall()[0])[0]
        decrypted_string = decrypt_string(unique_route_string.encode())
        sem = decrypted_string[5]
        student_class = decrypted_string[6:8]
        subject_fpsu_code = decrypted_string[8:]
        c.execute("""SELECT faculty.first_name, faculty.last_name, subject.subject_name
                    FROM pumis.faculty, pumis.subject
                    WHERE faculty.subject_fpsu_code=%s
                    AND faculty.class_alloted=%s
                    AND faculty.semester_alloted=%s""",(subject_fpsu_code, student_class, sem))
        resp = c.fetchall()
        faculty_firstname = resp[0][0]
        faculty_lastname = resp[0][1]
        subject_name = resp[0][2]
        c.close()
        conn.close()
        gc.collect()
        return render_template("chatbot.html")
    except Exception as e:
        return str(e)





if __name__ == "__main__":
    app.run()
