import json
import datetime

import module_funcs

####################################################################################################
#  MAIN

access = json.load(open('/home/gfot/cucm-cdr-analyzer/data/security/access.json'))  # Linux
body_file1 = '/home/gfot/cucm-cdr-analyzer/data/output/hourly_html.txt'
attachments1 = ['/home/gfot/cucm-cdr-analyzer/data/output/hourly_report.csv']
body_file2 = '/home/gfot/cucm-cdr-analyzer/data/output/daily_html.txt'
attachments2 = ['/home/gfot/cucm-cdr-analyzer/data/output/daily_report.csv']

current_date = datetime.datetime.now().strftime('%B %Y')

subject1 = "Hourly Call Report (Month Aggregate) - {}".format(current_date)
# subject1 = "Hourly Call Report (Month Aggregate) - November"
fd1 = open(body_file1, 'r')
body1 = fd1.read()
fd1.close()

subject2 = "Daily Call Report - {}".format(current_date)
# subject2 = "Daily Call Report - November"
fd2 = open(body_file2, 'r')
body2 = fd2.read()
fd2.close()

# Send e-mail
USERNAME = str(access["o365"]["username"])
PASSWORD = str(access["o365"]["password"])
MAIL_SERVER = str(access["o365"]["mail_server"])
toaddr = ["maricela.sandoval@amistadmp.org", "melanie.torres@vvrmc.org", \
          "michelle.silva@vvrmc.org", "Albert.Lattimer@vvrmc.org", "letty.ortiz@vvrmc.org", \
          "michael.zimmerman@vvrmc.org", "jorge.jurado@vvrmc.org"]
# toaddr = ["georgios.fotiadis@whitehatvirtual.com"]
module_funcs.send_mail(USERNAME, PASSWORD, MAIL_SERVER, toaddr, subject1, body1, attachments1, False, False)
module_funcs.send_mail(USERNAME, PASSWORD, MAIL_SERVER, toaddr, subject2, body2, attachments2, False, False)
