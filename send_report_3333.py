import smtplib
import json
import os
import sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
# from email import Encoders    # Python2

import send_mail

####################################################################################################
#  MAIN
subject = sys.argv[1]
body_file = sys.argv[2]
attachments = sys.argv[3]

# subject = "per hour"
# body_file = 'data/hourly_html.txt'
# attachments = 'data/hourly_report.csv'

access = json.load(open('data/access.json'))
USERNAME = str(access["gmail"]["username"])
PASSWORD = str(access["gmail"]["password"])

my_subject = "Call Report (%s)" % (subject)
fd = open(body_file,'r')
my_body = fd.read()
fd.close()

# toaddr = ["abhijit.dhar@whitehatvirtual.com","val.king@whitehatvirtual.com","floyd.willis@vvrmc.org", \
#           "john.lomas@vvrmc.org","dgalma01@vvrmc.org","maricela.sandoval@amistadmp.org","cgroom01@vvrmc.org", \
#           "Albert.Lattimer@vvrmc.org","Ricardo.Gonzalez@vvrmc.org","letty.ortiz@vvrmc.org","georgios.fotiadis@gmail.com"]
toaddr = ["georgios.fotiadis@gmail.com"]

send_mail.send_mail(USERNAME, PASSWORD, toaddr, my_subject, my_body, attachments)
