import json
import datetime

import _module_funcs

####################################################################################################
#  MAIN

# access = json.load(open('data/access.json'))                            # Windows
# body_file1 = 'data/hourly_html.txt'                                     # Windows
# attachments1 = ['data/hourly_report.csv']                               # Windows
# body_file2 = 'data/daily_html.txt'                                      # Windows
# attachments2 = ['data/daily_report.csv']                                # Windows

access = json.load(open('/home/pbx/cucm-cdr-analyzer/data/access.json'))  # Linux
body_file1 = '/home/pbx/cucm-cdr-analyzer/data/hourly_html.txt'           # Linux
attachments1 = ['/home/pbx/cucm-cdr-analyzer/data/hourly_report.csv']     # Linux
body_file2 = '/home/pbx/cucm-cdr-analyzer/data/daily_html.txt'            # Linux
attachments2 = ['/home/pbx/cucm-cdr-analyzer/data/daily_report.csv']      # Linux


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
USERNAME = str(access["gmail"]["username"])
PASSWORD = str(access["gmail"]["password"])
toaddr = ["abhijit.dhar@whitehatvirtual.com","val.king@whitehatvirtual.com","floyd.willis@vvrmc.org", \
          "john.lomas@vvrmc.org","dgalma01@vvrmc.org","maricela.sandoval@amistadmp.org","cgroom01@vvrmc.org", \
          "Albert.Lattimer@vvrmc.org","Ricardo.Gonzalez@vvrmc.org","letty.ortiz@vvrmc.org","georgios.fotiadis@whitehatvirtual.com"]
# toaddr = ["georgios.fotiadis@gmail.com"]
_module_funcs.send_mail(USERNAME, PASSWORD, toaddr, subject1, body1, attachments1)
_module_funcs.send_mail(USERNAME, PASSWORD, toaddr, subject2, body2, attachments2)
