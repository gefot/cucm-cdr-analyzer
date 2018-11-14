import json
import datetime

import _module_send_mail

####################################################################################################
#  MAIN
access = json.load(open('data/access.json'))
USERNAME = str(access["gmail"]["username"])
PASSWORD = str(access["gmail"]["password"])

current_date = datetime.datetime.now().strftime('%B %Y')

subject1 = "Hourly Call Report - {}".format(current_date)
body_file1 = 'data/hourly_html.txt'
fd1 = open(body_file1,'r')
body1 = fd1.read()
fd1.close()
attachments1 = ['data/hourly_report.csv']

subject2 = "DailyCall Report - {}".format(current_date)
body_file2 = 'data/daily_html.txt'
fd2 = open(body_file2,'r')
body2 = fd2.read()
fd2.close()
attachments2 = ['data/daily_report.csv']


# toaddr = ["abhijit.dhar@whitehatvirtual.com","val.king@whitehatvirtual.com","floyd.willis@vvrmc.org", \
#           "john.lomas@vvrmc.org","dgalma01@vvrmc.org","maricela.sandoval@amistadmp.org","cgroom01@vvrmc.org", \
#           "Albert.Lattimer@vvrmc.org","Ricardo.Gonzalez@vvrmc.org","letty.ortiz@vvrmc.org","georgios.fotiadis@gmail.com"]
toaddr = ["georgios.fotiadis@gmail.com"]
_module_send_mail.send_mail(USERNAME, PASSWORD, toaddr, subject1, body1, attachments1)
_module_send_mail.send_mail(USERNAME, PASSWORD, toaddr, subject2, body2, attachments2)
