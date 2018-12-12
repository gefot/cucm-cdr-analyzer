import json
import datetime

import module_funcs

####################################################################################################
#  MAIN

# access = json.load(open('data\\access.json'))                            # Windows
# body_file1 = 'data/output/hourly_html.txt'
# attachments1 = ['data/output/hourly_report.csv']
# body_file2 = 'data/output/daily_html.txt'
# attachments2 = ['data/output/daily_report.csv']

access = json.load(open('/home/pbx/cucm-cdr-analyzer/data/access.json'))  # Linux
body_file1 = '/home/pbx/cucm-cdr-analyzer/data/output/hourly_html.txt'
attachments1 = ['/home/pbx/cucm-cdr-analyzer/data/output/hourly_report.csv']
body_file2 = '/home/pbx/cucm-cdr-analyzer/data/output/daily_html.txt'
attachments2 = ['/home/pbx/cucm-cdr-analyzer/data/output/daily_report.csv']

current_date = datetime.datetime.now().strftime('%B %Y')

subject1 = "Hourly Call Report - {}".format(current_date)
fd1 = open(body_file1,'r')
body1 = fd1.read()
fd1.close()

subject2 = "Daily Call Report - {}".format(current_date)
fd2 = open(body_file2,'r')
body2 = fd2.read()
fd2.close()

# Send e-mail
USERNAME = str(access["o365"]["username"])
PASSWORD = str(access["o365"]["password"])
MAIL_SERVER = str(access["o365"]["mail_server"])
toaddr = ["abhijit.dhar@whitehatvirtual.com","val.king@whitehatvirtual.com","floyd.willis@vvrmc.org", \
          "john.lomas@vvrmc.org","dgalma01@vvrmc.org","maricela.sandoval@amistadmp.org","cgroom01@vvrmc.org", \
          "Albert.Lattimer@vvrmc.org","Ricardo.Gonzalez@vvrmc.org","letty.ortiz@vvrmc.org","georgios.fotiadis@whitehatvirtual.com"]
# toaddr = ["georgios.fotiadis@gmail.com"]
module_funcs.send_mail(USERNAME, PASSWORD, MAIL_SERVER, toaddr, subject1, body1, attachments1, False, False)
module_funcs.send_mail(USERNAME, PASSWORD, MAIL_SERVER, toaddr, subject2, body2, attachments2, False, False)
