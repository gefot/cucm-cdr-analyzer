import smtplib
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders    # Python2


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
    for attachment in attachments:
        # my_attachment = open(attachment, "rb")
        # file_name = os.path.basename(attachment)
        part2 = MIMEBase('application', 'octet-stream')
        part2.set_payload(open(attachment, "rb").read())
        part2.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment))
        encoders.encode_base64(part2)
        msg.attach(part2)
        # part2.set_payload(open(attachment, "rb").read())
        # print(attachment)
        # part2.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attachment))
        # encoders.encode_base64(part2)
        # msg.attach(part2)
        # print(part2)

    mailserver = smtplib.SMTP('smtp.gmail.com:587')
    #mailserver.ehlo()
    mailserver.starttls()
    #mailserver.ehlo()
    mailserver.login(username, password)
    mailserver.sendmail(fromaddr, toaddr, msg.as_string())
    mailserver.quit()
