import smtplib
import json
import os
import sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
# from email import Encoders    # Python2


def send_mail(username, password, toaddr, subject, body, attachment):

    fromaddr = username
    #text = "This will be sent as text"

    msg = MIMEMultipart()
    msg['To'] = ", ".join(toaddr)
    msg['From'] = fromaddr
    msg['Subject'] = subject

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attachment, "rb").read())
    # Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attachment))
    msg.attach(part)

    #part1 = MIMEText(text, 'plain')
    part2 = MIMEText(body, 'html')
    #msg.attach(part1)
    msg.attach(part2)

    mailserver = smtplib.SMTP('smtp.gmail.com:587')
    #mailserver.ehlo()
    mailserver.starttls()
    #mailserver.ehlo()
    mailserver.login(username, password)
    mailserver.sendmail(fromaddr, toaddr, msg.as_string())
    mailserver.close()

####################################################################################################
#  MAIN
subject = sys.argv[1]
body_file = sys.argv[2]
attachment = sys.argv[3]

# subject = "per hour"
# body_file = 'data/hourly_html.txt'
# attachment = 'data/hourly_report.csv'

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

send_mail(USERNAME, PASSWORD, toaddr, my_subject, my_body, attachment)
