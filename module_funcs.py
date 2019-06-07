import os
import re
import datetime

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import ftplib

import classes


# Starting from index 1:
# 3:  globalCallID_callId
# 5:  Date (in UTC timezone)
# 9:  calling number
# 30: called number
# 31: final called number
# 50: lastRedirectDn
# 56: duration
# 57: origDeviceName
# 58: destDeviceName


###########################################################################################################################################
def is_cdr_date(date, clinic):
    hour = int(date.strftime('%H'))
    weekday = date.weekday()

    ### Main Hospital Business Hours
    if (clinic == "main" and (
            weekday == 0 or weekday == 1 or weekday == 2 or weekday == 3 or weekday == 4 or weekday == 5 or weekday == 6) and (hour >= 6 and hour <= 21)):
        return True

    ### Shannon Clinic Business Hours
    if (clinic == "shannon" and (
            ((weekday == 0 or weekday == 1 or weekday == 2 or weekday == 3) and (hour >= 8 and hour <= 16)) or ((weekday == 4) and (hour >= 8 and hour <= 11)))):
        return True

    ### Lyndsey Clinic Business Hours
    if (clinic == "lyndsey" and (
            ((weekday == 0 or weekday == 1 or weekday == 2 or weekday == 3) and (hour >= 8 and hour <= 16)) or ((weekday == 4) and (hour >= 8 and hour <= 15)))):
        return True

    return False


###########################################################################################################################################
def is_call_tree_option(hunt_pilot):
    """
    :param hunt_pilot: Hunt-pilot to categorize; it has to be unique so as to differentiate call trees
    :return: call tree option selected
    """

    aa_option = -1

    ### 1801 AA options
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
def categorize_cdr(cdr_record, call_tree):
    """
    :param cdr_record: the CDR record to analyze
    :param call_tree: the call tree (eg. main, shannon, lyndsey)
    :return:
    """

    cdr_call = None

    date = cdr_record.date
    called_num = cdr_record.called_num
    final_called_num = cdr_record.final_called_num
    last_redirect_num = cdr_record.last_redirect_num
    duration = cdr_record.duration

    ### Main Call Tree
    if call_tree == "main":
        if is_cdr_date(date, call_tree):
            if called_num == "1001":
                if int(duration) == 0:
                    cdr_call = classes.CategorizedCall("1st", "missed")
                    cdr_call.cdr_record = cdr_record
                elif (
                        final_called_num == "1001" or final_called_num == "5701" or final_called_num == "5702" or final_called_num == "5703" or final_called_num == "5704" or final_called_num == "5705") and int(
                    duration) > 0:
                    cdr_call = classes.CategorizedCall("1st", "answered")
                    cdr_call.answered_by = cdr_record.destDeviceName
                    cdr_call.cdr_record = cdr_record
                elif final_called_num == "5500" and last_redirect_num == "5800" and int(duration) > 0:
                    cdr_call = classes.CategorizedCall("aa", "missed")
                    cdr_call.cdr_record = cdr_record

    ### 1801 Call Tree
    elif call_tree == "shannon":
        if is_cdr_date(date, call_tree):
            if called_num == "5810":
                if called_num == "5810" and final_called_num == "5810" and last_redirect_num == "5810" and int(duration) == 0:
                    cdr_call = classes.CategorizedCall("1st", "missed")
                    cdr_call.cdr_record = cdr_record
                elif called_num == "5810" and final_called_num == "5810" and last_redirect_num == "5810" and int(duration) > 0:
                    cdr_call = classes.CategorizedCall("1st", "answered")
                    cdr_call.answered_by = cdr_record.destDeviceName
                    cdr_call.cdr_record = cdr_record
                elif called_num == "5810" and final_called_num == "5500" and last_redirect_num == "5811":
                    cdr_call = classes.CategorizedCall("aa", "missed")
                    cdr_call.cdr_record = cdr_record

    return cdr_call


###########################################################################################################################################
def categorize_cdr_aa(cdr_record):
    """
    :param cdr_record: class CDRRecord
    :return: the call info as dictionary (fields: type, handle, answered_by, option
    """

    cdr_call = None

    if is_call_tree_option(cdr_record.called_num) > -1:
        if is_call_tree_option(cdr_record.called_num) > -1 and is_call_tree_option(cdr_record.final_called_num) > -1 and cdr_record.last_redirect_num == "5500" and int(
                cdr_record.duration) == 0:
            cdr_call = classes.CategorizedCall("aa", "missed")
            cdr_call.cdr_record_aa = cdr_record
        elif is_call_tree_option(cdr_record.called_num) > -1 and is_call_tree_option(cdr_record.final_called_num) > -1 and cdr_record.last_redirect_num == "5500" and int(
                cdr_record.duration) > 0:
            cdr_call = classes.CategorizedCall("aa", "answered")
            cdr_call.answered_by = cdr_record.destDeviceName
            cdr_call.option = is_call_tree_option(cdr_record.called_num)
            cdr_call.cdr_record_aa = cdr_record
        elif is_call_tree_option(cdr_record.called_num) > -1 and cdr_record.final_called_num == "5500":
            cdr_call = classes.CategorizedCall("aa", "missed")
            cdr_call.answered_by = "VM" + cdr_record.last_redirect_num
            cdr_call.option = is_call_tree_option(cdr_record.called_num)
            cdr_call.cdr_record_aa = cdr_record

    return cdr_call


###########################################################################################################################################
def categorize_cdr_general(cdr_file_list, call_tree):
    """
    :param cdr_file_list: files of files with cdr records
    :param call_tree:
    :return: list CategorizedCall objects
    """

    categorized_calls = []
    try:
        for file in cdr_file_list:
            fd = open(file, "r")
            for line in fd:
                try:
                    list = line.split(',')
                    cdr_record = classes.CDRRecord(list[2], datetime.datetime.fromtimestamp(int(list[4])), list[8].strip("\""), list[29].strip("\""),
                                                   list[30].strip("\""), list[49].strip("\""),
                                                   list[55], list[56].strip("\""), list[57].strip("\""))
                    categorized_call = categorize_cdr(cdr_record, call_tree)

                    if categorized_call is not None:
                        categorized_calls.append(categorized_call)

                    ### Further categorize CDR calls, that where answered by call-tree
                    ### Presently it is done only for Shannon
                    if call_tree == "shannon":
                        if categorized_call.type == "aa":
                            fd_tmp = open(file, "r")
                            found_1st_time = False
                            found_2nd_time = False
                            my_line = ""
                            ### Re-parse CDR file to search for AA global ID
                            for line_tmp in fd_tmp:
                                try:
                                    list_tmp = line_tmp.split(',')
                                    if list_tmp[2] == list[2] and not found_1st_time and not found_2nd_time:
                                        found_1st_time = True
                                        continue
                                    if list_tmp[2] == list[2] and found_1st_time and not found_2nd_time:
                                        found_2nd_time = True
                                        my_line = line_tmp
                                        break
                                except Exception as ex:
                                    pass
                            fd_tmp.close()

                            if found_2nd_time:
                                list_tmp = my_line.split(',')
                                cdr_record_tmp = classes.CDRRecord(list_tmp[2], datetime.datetime.fromtimestamp(int(list_tmp[4])), list_tmp[8].strip("\""),
                                                                   list_tmp[29].strip("\""),
                                                                   list_tmp[30].strip("\""), list_tmp[49].strip("\""),
                                                                   list_tmp[55], list_tmp[56].strip("\""), list_tmp[57].strip("\""))
                                categorized_call_tmp = categorize_cdr_aa(cdr_record_tmp)

                                categorized_call.handle = categorized_call_tmp.handle
                                categorized_call.answered_by = categorized_call_tmp.answered_by
                                categorized_call.option = categorized_call_tmp.option
                                categorized_call.cdr_record_aa = categorized_call_tmp.cdr_record_aa

                except Exception as ex:
                    pass
                    # break
            fd.close()

    except Exception as ex:
        print(ex)

    return categorized_calls


###########################################################################################################################################
def generate_reports(startdate, enddate, categorized_calls):
    print(startdate)
    print(enddate)

    counted_calls_daily = {'total': [0 for i in range(32)], 'answered_1st': [0 for i in range(32)], 'answered_aa': [0 for i in range(32)],
                           'missed': [0 for i in range(32)], 'missed_aa_vm': [0 for i in range(32)]}
    counted_calls_hourly = {'total': [0 for i in range(24)], 'answered_1st': [0 for i in range(24)], 'answered_aa': [0 for i in range(32)],
                            'missed': [0 for i in range(24)], 'missed_aa_vm': [0 for i in range(24)]}

    for call in categorized_calls:
        date = call.cdr_record.date
        hour = int(date.strftime('%H'))
        day = int(date.strftime('%d'))
        weekday = date.weekday()

        counted_calls_daily['total'][day] += 1
        counted_calls_daily['total'][0] += 1
        counted_calls_hourly['total'][hour] += 1
        counted_calls_hourly['total'][0] += 1

        if call.type == "1st" and call.handle == "answered":
            counted_calls_daily['answered_1st'][day] += 1
            counted_calls_daily['answered_1st'][0] += 1

            counted_calls_hourly['answered_1st'][hour] += 1
            counted_calls_hourly['answered_1st'][0] += 1

        elif call.type == "aa" and call.handle == "answered":
            counted_calls_daily['answered_aa'][day] += 1
            counted_calls_daily['answered_aa'][0] += 1

            counted_calls_hourly['answered_aa'][hour] += 1
            counted_calls_hourly['answered_aa'][0] += 1

        elif (call.type == "1st" or call.type == "aa") and call.handle == "missed" and "VM" not in call.answered_by:
            counted_calls_daily['missed'][day] += 1
            counted_calls_daily['missed'][0] += 1

            counted_calls_hourly['missed'][hour] += 1
            counted_calls_hourly['missed'][0] += 1

        elif call.type == "aa" and call.handle == "missed" and "VM" in call.answered_by:
            counted_calls_daily['missed_aa_vm'][day] += 1
            counted_calls_daily['missed_aa_vm'][0] += 1

            counted_calls_hourly['missed_aa_vm'][hour] += 1
            counted_calls_hourly['missed_aa_vm'][0] += 1

        # print(date)
        # print(hour)
        # print(day)
        # print(weekday)

    return counted_calls_daily, counted_calls_hourly


###########################################################################################################################################
def create_reports_csv(filename, type, counted_calls):

    print(counted_calls['total'])

    csv_text = ""

    for i, val in enumerate(counted_calls['total']):
        csv_text += "{}, ".format(i)
        # print(counted_calls['answered_1st'][i])
        # print(counted_calls['answered_aa'][i])
        # print(counted_calls['missed'][i])
        # print(counted_calls['missed_aa_vm'][i])

    print(csv_text)

    # fd = open(filename, "w")
    # fd.write(csv_text)
    # fd.close()


###########################################################################################################################################
def get_cdr_records(cdr_file_list, filters):
    extensions = filters['extensions']

    cdr_records = []

    ### Parse CDR file
    try:
        for cdr_file in cdr_file_list:
            # print("\n\n\n {}".format(file))
            fd = open(cdr_file, "r")
            for line in fd:
                try:
                    list = line.split(',')
                    for extension in extensions:
                        if extension == "*":
                            cdr_record = classes.CDRRecord(list[2], datetime.datetime.fromtimestamp(int(list[4])), list[8].strip("\""), list[29].strip("\""),
                                                           list[30].strip("\""), list[49].strip("\""),
                                                           list[55], list[56].strip("\""), list[57].strip("\""))
                            cdr_records.append(cdr_record)
                        elif list[8] == "\"" + extension + "\"" or list[29] == "\"" + extension + "\"":
                            cdr_record = classes.CDRRecord(list[2], datetime.datetime.fromtimestamp(int(list[4])), list[8].strip("\""), list[29].strip("\""),
                                                           list[30].strip("\""), list[49].strip("\""),
                                                           list[55], list[56].strip("\""), list[57].strip("\""))
                            cdr_records.append(cdr_record)
                except Exception as ex:
                    pass
                    # break
            fd.close()
    except Exception as ex:
        print(ex)

    return cdr_records


###########################################################################################################################################
def get_cdr_files(startdate, enddate):
    CDR_CURRENT = '/home/gfot/cdr/cdr_data/'
    CDR_ARCHIVE = '/home/gfot/cdr/cdr_archive/'
    TIMEZONE = +5

    now = datetime.datetime.now()
    nowdate = now.strftime("%Y%m")

    ### Shift dates to GMT so as to match CDR
    startdate_short = re.search(r'(\d{6})', startdate).group(1)
    startdate_obj = datetime.datetime.strptime(startdate, '%Y%m%d%H%M')
    startdate_obj_new = startdate_obj + datetime.timedelta(hours=TIMEZONE)
    startdate_new = datetime.datetime.strftime(startdate_obj_new, '%Y%m%d%H%M')

    enddate_short = re.search(r'(\d{6})', enddate).group(1)
    enddate_obj = datetime.datetime.strptime(enddate, '%Y%m%d%H%M')
    enddate_obj_new = enddate_obj + datetime.timedelta(hours=TIMEZONE)
    enddate_new = datetime.datetime.strftime(enddate_obj_new, '%Y%m%d%H%M')

    ### Construct CDR folder
    cdr_folder = []
    if nowdate in startdate_new or nowdate in enddate_new:
        cdr_folder.append(CDR_CURRENT)
    for folder in os.listdir(CDR_ARCHIVE):
        if startdate_short <= folder <= enddate_short:
            cdr_folder.append(CDR_ARCHIVE + folder + "/")

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
    # mailserver.ehlo()
    if tls:
        mailserver.starttls()
    # mailserver.ehlo()
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


###########################################################################################################################################
###########################################################################################################################################
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
###########################################################################################################################################
###########################################################################################################################################
