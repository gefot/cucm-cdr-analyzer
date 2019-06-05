import smtplib
import os
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import ftplib

import datetime


###########################################################################################################################################
def is_cdr_date(date, clinic):
    # print(date)
    hour = int(date.strftime('%H'))
    weekday = date.weekday()

    # Main Hospital Business Hours
    if (clinic == "main" and (
            weekday == 0 or weekday == 1 or weekday == 2 or weekday == 3 or weekday == 4 or weekday == 5 or weekday == 6) and (hour >= 6 and hour <= 21)):
        return True

    # Shannon Clinic Business Hours
    if (clinic == "shannon" and (
            ((weekday == 0 or weekday == 1 or weekday == 2 or weekday == 3) and (hour >= 8 and hour <= 16)) or ((weekday == 4) and (hour >= 8 and hour <= 11)))):
        return True

    # Lyndsey Clinic Business Hours
    if (clinic == "lyndsey" and (
            ((weekday == 0 or weekday == 1 or weekday == 2 or weekday == 3) and (hour >= 8 and hour <= 16)) or ((weekday == 4) and (hour >= 8 and hour <= 15)))):
        return True

    return False


###########################################################################################################################################
def is_call_tree_option(hunt_pilot):

    aa_option = -1

    # 1801 AA options
    if hunt_pilot == "5819":
        aa_option = 0
    if hunt_pilot == "5816":
        aa_option = 2
    elif hunt_pilot == "5823":
        aa_option = 3
    elif hunt_pilot == "5817":
        aa_option = 4
    elif hunt_pilot == "5818":
        aa_option = 5
    elif hunt_pilot == "5820":
        aa_option = 6
    elif hunt_pilot == "5822":
        aa_option = 7

    return aa_option


###########################################################################################################################################
def categorize_cdr(cdr_record):
    """
    This function differentiates between clinic
    """

    cdr_call = {}

    # 1801 Call Tree
    if is_cdr_date(cdr_record.date, "shannon"):
        if cdr_record.called_num == "5810":
            if cdr_record.called_num == "5810" and cdr_record.final_called_num == "5810" and cdr_record.last_redirect_num == "5810" and int(cdr_record.duration) == 0:
                cdr_call['type'] = "1st level"
                cdr_call['handle'] = "unanswered"
                cdr_call['answered_by'] = "None"
            elif cdr_record.called_num == "5810" and cdr_record.final_called_num == "5810" and cdr_record.last_redirect_num == "5810" and int(cdr_record.duration) > 0:
                cdr_call['type'] = "1st level"
                cdr_call['handle'] = "answered"
                cdr_call['answered_by'] = cdr_record.destDeviceName
            elif cdr_record.called_num == "5810" and cdr_record.final_called_num == "5500" and cdr_record.last_redirect_num == "5811":
                cdr_call['type'] = "aa"
                cdr_call['handle'] = "unanswered"
                cdr_call['answered_by'] = "None"
            # print("\n")
            # print(cdr_record)
            # print(cdr_call)
    return cdr_call


def categorize_cdr_aa(cdr_record):
    """
    This function categorizes depending on Hunt Pilot
    """

    cdr_call = {}

    # 1801 AA Call further categorization
    if is_call_tree_option(cdr_record.called_num) > -1:
        if is_call_tree_option(cdr_record.called_num) > -1 and is_call_tree_option(cdr_record.final_called_num) > -1 and cdr_record.last_redirect_num == "5500" and int(cdr_record.duration) == 0:
            cdr_call['type'] = "aa"
            cdr_call['handle'] = "unanswered"
            cdr_call['answered_by'] = "None"
        elif is_call_tree_option(cdr_record.called_num) > -1 and is_call_tree_option(cdr_record.final_called_num) > -1 and cdr_record.last_redirect_num == "5500" and int(cdr_record.duration) > 0:
            cdr_call['type'] = "aa"
            cdr_call['handle'] = "answered"
            cdr_call['answered_by'] = cdr_record.destDeviceName
            cdr_call['option'] = is_call_tree_option(cdr_record.called_num)
        elif is_call_tree_option(cdr_record.called_num) > -1 and cdr_record.final_called_num == "5500":
            cdr_call['type'] = "aa"
            cdr_call['handle'] = "unanswered"
            cdr_call['answered_by'] = "VM" + cdr_record.last_redirect_num
            cdr_call['option'] = is_call_tree_option(cdr_record.called_num)
        # print("\n")
        # print(cdr_record)
        # print(cdr_call)
    return cdr_call


###########################################################################################################################################
def create_html_file(total_calls, answered_calls, aa_calls, unanswered_calls, total_calls_list, answered_calls_list,
                     aa_calls_list, unanswered_calls_list, answered_calls_per_list, aa_calls_per_list,
                     unanswered_calls_per_list, filename, clinic_names, start, end):
    html_text = """<HTML>
<HEAD>
<STYLE>
td {
    text-align:center;
    padding:4px;
}
</STYLE>
</HEAD>
<BODY>"""

    for key in total_calls_list.keys():
        html_text += "<hr>"
        html_text += "<p>" + clinic_names[key] + "</p>\n"

        html_text += "<TABLE>\n"

        html_text += "<TR>\n"
        html_text += "<TD><b></b></TD>"
        for i in range(start, end):
            html_text += "<TD><b>" + str(i) + "</b></TD>"
        html_text += "<TD><b>Total</b></TD>"
        html_text += "\n</TR>\n"

        html_text += "<TR>"
        html_text += "\n<TD>Calls Answered #</TD>"
        for i in range(start, end):
            html_text += "<TD>" + str(answered_calls_list[key][i]) + "</TD>"
        html_text += "<TD>" + str(answered_calls[key]) + "</TD>"
        html_text += "\n</TR>\n"

        html_text += "<TR>"
        html_text += "\n<TD>Calls Answered %</TD>"
        for i in range(start, end):
            html_text += "<TD>" + str(answered_calls_per_list[key][i]) + "%</TD>"
        html_text += "<TD>" + str(round(float(answered_calls[key]) / total_calls[key] * 100, 1)) + "%</TD>"
        html_text += "\n</TR>\n"

        html_text += "<TR>"
        html_text += "\n<TD>Auto Attendant #</TD>"
        for i in range(start, end):
            html_text += "<TD>" + str(aa_calls_list[key][i]) + "</TD>"
        html_text += "<TD>" + str(aa_calls[key]) + "</TD>"
        html_text += "\n</TR>\n"

        html_text += "<TR>"
        html_text += "\n<TD>Auto Attendant %</TD>"
        for i in range(start, end):
            html_text += "<TD>" + str(aa_calls_per_list[key][i]) + "%</TD>"
        html_text += "<TD>" + str(round(float(aa_calls[key]) / total_calls[key] * 100, 1)) + "%</TD>"
        html_text += "\n</TR>\n"

        html_text += "<TR>"
        html_text += "\n<TD>Calls Unanswered #</TD>"
        for i in range(start, end):
            html_text += "<TD>" + str(unanswered_calls_list[key][i]) + "</TD>"
        html_text += "<TD>" + str(unanswered_calls[key]) + "</TD>"
        html_text += "\n</TR>\n"

        html_text += "<TR>"
        html_text += "\n<TD>Calls Unanswered %</TD>"
        for i in range(start, end):
            html_text += "<TD>" + str(unanswered_calls_per_list[key][i]) + "%</TD>"
        html_text += "<TD>" + str(round(float(unanswered_calls[key]) / total_calls[key] * 100, 1)) + "%</TD>"
        html_text += "\n</TR>\n"

        html_text += "<TR>"
        html_text += "\n<TD><b>Call Volume</b></TD>"
        for i in range(start, end):
            html_text += "<TD><b>" + str(total_calls_list[key][i]) + "</b></TD>"
        html_text += "<TD><b>" + str(total_calls[key]) + "</b></TD>"
        html_text += "\n</TR>\n"

        html_text += "</TABLE>\n"

        html_text += "\n</BODY>\n</HTML>\n"
    html_text += "<hr>"

    fd = open(filename, "w")
    fd.write(html_text)
    fd.close()

    return 0


###########################################################################################################################################
def create_csv_file(total_calls, answered_calls, aa_calls, unanswered_calls, total_calls_list, answered_calls_list,
                    aa_calls_list, unanswered_calls_list, answered_calls_per_list, aa_calls_per_list,
                    unanswered_calls_per_list, filename, clinic_names, start, end):
    csv_text = ""

    for key in total_calls_list.keys():
        csv_text += "\n" + clinic_names[key]

        csv_text += ","
        for i in range(start, end):
            csv_text += str(i) + ","
        csv_text += "Total\n"

        csv_text += "Calls Answered #,"
        for i in range(start, end):
            csv_text += str(answered_calls_list[key][i]) + ","
        csv_text += str(answered_calls[key]) + "\n"
        csv_text += "Calls Answered %,"
        for i in range(start, end):
            csv_text += str(answered_calls_per_list[key][i]) + ","
        if total_calls[key] > 0:
            csv_text += str(round(float(answered_calls[key]) / total_calls[key] * 100, 1)) + "\n"
        else:
            csv_text += "<TD>" + "0.0" + "%</TD>"

        csv_text += "Auto Attendant #,"
        for i in range(start, end):
            csv_text += str(aa_calls_list[key][i]) + ","
        csv_text += str(aa_calls[key]) + "\n"
        csv_text += "Auto Attendant %,"
        for i in range(start, end):
            csv_text += str(aa_calls_per_list[key][i]) + ","
        if total_calls[key] > 0:
            csv_text += str(round(float(aa_calls[key]) / total_calls[key] * 100, 1)) + "\n"
        else:
            csv_text += "<TD>" + "0.0" + "%</TD>"

        csv_text += "Calls Unanswered #,"
        for i in range(start, end):
            csv_text += str(unanswered_calls_list[key][i]) + ","
        csv_text += str(unanswered_calls[key]) + "\n"
        csv_text += "Calls Unanswered %,"
        for i in range(start, end):
            csv_text += str(unanswered_calls_per_list[key][i]) + ","
        if total_calls[key] > 0:
            csv_text += str(round(float(unanswered_calls[key]) / total_calls[key] * 100, 1)) + "\n"
        else:
            csv_text += "<TD>" + "0.0" + "%</TD>"

        csv_text += "Call Volume,"
        for i in range(start, end):
            csv_text += str(total_calls_list[key][i]) + ","
        csv_text += str(total_calls[key]) + "\n"

    fd = open(filename, "w")
    fd.write(csv_text)
    fd.close()

    return 0


###########################################################################################################################################
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


###########################################################################################################################################
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


###########################################################################################################################################
def get_files_ftp(server, username, password, source_path, dest_path, pattern):
    ftp = ftplib.FTP(server, username, password)
    ftp.cwd(source_path)
    file_list = ftp.nlst()

    for file in file_list:
        if re.match(pattern, file):
            with open(dest_path + file, 'wb') as my_file:
                op = ftp.retrbinary('RETR %s' % file, my_file.write)
    ftp.quit()

###########################################################################################################################################
