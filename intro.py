from mysql_dbconnect import *
from secret_hash import *
import gc

def get_data(unique_route_string):
    c, conn = connect_to()
    c.execute("SELECT student.first_name FROM pumis.student, fpsu.route_string WHERE route_string.string=%s AND route_string.enrollment_number=student.enrollment_number", (unique_route_string))
    student_firstname = (c.fetchall()[0])[0]
    decrypted_string = decrypt_string(unique_route_string.encode())
    sem = decrypted_string[5]
    student_class = decrypted_string[6:8]
    subject_fpsu_code = decrypted_string[8:]
    c.execute("""SELECT faculty.first_name, faculty.last_name
                FROM pumis.faculty
                WHERE faculty.subject_fpsu_code=%s
                AND faculty.class_alloted=%s
                AND faculty.semester_alloted=%s""",(subject_fpsu_code, student_class, sem))
    resp = c.fetchall()
    faculty_firstname = resp[0][0]
    faculty_lastname = resp[0][1]
    faculty_fullname = faculty_firstname + " " + faculty_lastname
    c.close()
    conn.close()
    gc.collect()

    return [decrypted_string,student_firstname, faculty_fullname]
