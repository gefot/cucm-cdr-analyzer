import smtplib
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
# from email import Encoders    # Python2


def send_mail(username, password, toaddr, subject, body, attachments):

    fromaddr = username
    # text = "This will be sent as text"

    msg = MIMEMultipart()
    msg['To'] = ", ".join(toaddr)
    msg['From'] = fromaddr
    msg['Subject'] = subject

    # Attach e-mail body
    #part1 = MIMEText(text, 'plain')
    part1 = MIMEText(body, 'html')
    msg.attach(part1)

    # Attach e-mail attachments
    part2 = MIMEBase('application', 'octet-stream')
    for attachment in attachments:
        part2.set_payload(open(attachment, "rb").read())
        # Encoders.encode_base64(part)
        part2.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attachment))
        # print(attachment)
        msg.attach(part2)

    mailserver = smtplib.SMTP('smtp.gmail.com:587')
    #mailserver.ehlo()
    mailserver.starttls()
    #mailserver.ehlo()
    mailserver.login(username, password)
    mailserver.sendmail(fromaddr, toaddr, msg.as_string())
    mailserver.close()
