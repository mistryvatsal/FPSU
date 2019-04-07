import gmail
from mysql_dbconnect import *
import datetime

c, conn = connection_to_pumis();
c.execute('SELECT email_id FROM student')
email_ids = c.fetchall()
email_ids_list = list()
for i in email_ids:
    for j in i:
        email_ids_list.append(str(j))
earlier_list = ["aninditaguha9@gmail.com", "jahnvimehta20@gmail.com", "mistryvatsal11@gmail.com", "prarthana273@gmail.com", "HARSHGP44@GMAIL.COM", "krupapatel1005@gmail.com", "sutharsweety27@gmail.com", "shivanshis816@gmail.com", "sanskritishukla94001@gmail.com"]
subject = 'Feedback Form 1'
#body = 'Hey there, \n This is a test mail from CodingPrivacy. Thankyou for registering yourself to the feedback system project development phase.\n Stay tuned for feedback form filling.\n We are thankful to you for joining.\n\n\n\n CodingPrivacy.'
bodyHTML = 'Hey there, <br><br>We request you to please fill the feedback form by clicking <a href = "http://157.230.155.9/feedback_desc/">here</a>.<br><br><br>CodingPrivacy.'
f = open("email.log", "a+")
#for i in email_ids_list:
    #if i not in earlier_list:
gmail.send_message("nitindlalwani@gmail.com", subject, bodyHTML)
f.write( "nitindlalwani@gmail.com" + " " + subject + " " + str(datetime.datetime.utcnow()))
