import smtplib
import os
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import ftplib

import datetime


def is_cdr_date(date, clinic):

    # print(date)
    hour = int(date.strftime('%H'))
    weekday = date.weekday()

    # Main Hospital Business Hours
    if (clinic == "main" and (
            weekday == 0 or weekday == 1 or weekday == 2 or weekday == 3 or weekday == 4 or weekday == 5 or weekday == 6) and (
            hour >= 6 and hour <= 21)):
        return True

    # Shannon Clinic Business Hours
    if (clinic == "shannon" and (
            ((weekday == 0 or weekday == 1 or weekday == 2 or weekday == 3) and (hour >= 8 and hour <= 16)) or (
            (weekday == 4) and (hour >= 8 and hour <= 11)))):
        return True

    # Lyndsey Clinic Business Hours
    if (clinic == "lyndsey" and (
            ((weekday == 0 or weekday == 1 or weekday == 2 or weekday == 3) and (hour >= 8 and hour <= 16)) or (
            (weekday == 4) and (hour >= 8 and hour <= 15)))):
        return True

    return False

def send_mail(username, password, mail_server, toaddr, subject, body, attachments, login, tls):
    fromaddr = username
    # text = "This will be sent as text"

    msg = MIMEMultipart()
    msg['To'] = ", ".join(toaddr)
    msg['From'] = fromaddr
    msg['Subject'] = subject

    ### Attach e-mail body
    # part1 = MIMEText(text, 'plain')
    part1 = MIMEText(body, 'html')
    msg.attach(part1)

    ### Attach e-mail attachments
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

    mailserver = smtplib.SMTP(mail_server)
    ##mailserver.ehlo()
    if tls:
        mailserver.starttls()
    ##mailserver.ehlo()
    if login:
        mailserver.login(username, password)
    mailserver.sendmail(fromaddr, toaddr, msg.as_string())
    mailserver.quit()


def get_files_ftp(server, username, password, source_path, dest_path, pattern):
    ftp = ftplib.FTP(server, username, password)
    ftp.cwd(source_path)
    file_list = ftp.nlst()

    for file in file_list:
        if re.match(pattern, file):
            with open(dest_path + file, 'wb') as my_file:
                op = ftp.retrbinary('RETR %s' % file, my_file.write)
    ftp.quit()


def get_cdr_files(startdate, enddate):
    CDR_CURRENT = '/home/gfot/cdr/cdr_data/'
    CDR_ARCHIVE = '/home/gfot/cdr/cdr_archive/'
    TIMEZONE = +5

    now = datetime.datetime.now()
    nowdate = now.strftime("%Y%m")

    ### Shift dates to GMT so as to much CDR
    startdate_short = re.search(r'(\d{6})', startdate).group(1)
    startdate_obj = datetime.datetime.strptime(startdate, '%Y%m%d%H%M')
    startdate_obj_new = startdate_obj + datetime.timedelta(hours=TIMEZONE)
    startdate_new = datetime.datetime.strftime(startdate_obj_new, '%Y%m%d%H%M')
    # print("local time = ", startdate)
    # print("GMT time = ", startdate_new)

    enddate_short = re.search(r'(\d{6})', enddate).group(1)
    enddate_obj = datetime.datetime.strptime(enddate, '%Y%m%d%H%M')
    enddate_obj_new = enddate_obj + datetime.timedelta(hours=TIMEZONE)
    enddate_new = datetime.datetime.strftime(enddate_obj_new, '%Y%m%d%H%M')
    # print("local time = ", enddate)
    # print("GMT time = ", enddate_new)

    ### Construct CDR folder
    cdr_folder = []
    if nowdate in startdate_new or nowdate in enddate_new:
        cdr_folder.append(CDR_CURRENT)
    for folder in os.listdir(CDR_ARCHIVE):
        if startdate_short <= folder <= enddate_short:
            cdr_folder.append(CDR_ARCHIVE + folder + "/")
    # print("CDR_FOLDER = {}".format(cdr_folder))

    ### Get CDR files according to start and end dates
    cdr_file_list = []
    for my_folder in cdr_folder:
        for filename in os.listdir(my_folder):
            if filename.startswith("cdr") and "_01_" in filename:
                cdr_pattern = re.search(r'cdr_\w*_\d{2}_(\d{12})', filename).group(1)
                if int(cdr_pattern) > int(startdate_new) and int(cdr_pattern) < int(enddate_new):
                    cdr_file_list.append(my_folder + filename)
    cdr_file_list.sort()

    return cdr_file_list
