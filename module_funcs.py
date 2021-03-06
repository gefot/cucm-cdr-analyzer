import re
import os
import datetime
import time
import sqlite3
import csv

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import ftplib

import classes

CDR_REPO = '/home/gfot/cdr/cdr_repo/'
CDR_ARCHIVE = '/home/gfot/cdr/cdr_archive/'
CDR_DB = "/home/gfot/cucm-cdr-analyzer/cucm.db"


####################################################################################################
def populate_db():

    try:
        conn = sqlite3.connect(CDR_DB)
        cursor = conn.cursor()

        for filename in os.listdir(CDR_REPO):
            # if filename.startswith("cdr") and "_01_" in filename:
            if filename.startswith("cdr"):
                fd = open(CDR_REPO + filename, "r")
                for line in fd:
                    try:
                        my_list = line.split(',')
                        # recordType = my_list[0]
                        # globalCallID_callManagerId = my_list[1]
                        globalCallID_callId = my_list[2]
                        # Ignore line if it is the beginning of a file
                        if not globalCallID_callId.isnumeric():
                            continue
                        origLegCallIdentifier = my_list[3]
                        destLegIdentifier = my_list[25]
                        dateTimeOrigination = my_list[4]
                        callingPartyNumber = my_list[8].strip("\"")
                        originalCalledPartyNumber = my_list[29].strip("\"")
                        finalCalledPartyNumber = my_list[30].strip("\"")
                        lastRedirectDn = my_list[49].strip("\"")
                        duration = my_list[55].strip("\"")
                        origDeviceName = my_list[56].strip("\"")
                        destDeviceName = my_list[57].strip("\"")
                        huntPilotDN = my_list[102].strip("\"")

                        # origNodeId = my_list[5]
                        # origSpan = my_list[6]         # Not needed
                        # origIpAddr = my_list[7]       # Not needed (hex)
                        # destNodeId = my_list[26]
                        # destSpan = my_list[27]        # Not needed
                        # destIpAddr = my_list[28]      # Not needed (hex)
                        # globalCallId_ClusterID = my_list[65]  # Always the same

                        # print("{},{},{},{},{},{},{},{},{},{},{},{}".format(
                        #     globalCallID_callId,
                        #     origLegCallIdentifier,
                        #     destLegIdentifier,
                        #     dateTimeOrigination,
                        #     callingPartyNumber,
                        #     originalCalledPartyNumber,
                        #     finalCalledPartyNumber,
                        #     lastRedirectDn,
                        #     duration,
                        #     origDeviceName,
                        #     destDeviceName,
                        #     huntPilotDN)
                        # )
                        try:
                            insert = "INSERT INTO CDR VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                                globalCallID_callId,
                                origLegCallIdentifier,
                                destLegIdentifier,
                                dateTimeOrigination,
                                callingPartyNumber,
                                originalCalledPartyNumber,
                                finalCalledPartyNumber,
                                lastRedirectDn,
                                duration,
                                origDeviceName,
                                destDeviceName,
                                huntPilotDN)
                            cursor.execute(insert)
                        except:
                            print("Primary Key Error:", globalCallID_callId)
                            continue
                    except Exception as ex:
                        continue

                fd.close()

        conn.commit()
        conn.close()

    except Exception as ex:
        print(ex)

    # Move file from REPO to ARCHIVE
    print("Moving Files!!!")
    for filename in os.listdir(CDR_REPO):
        try:
            os_command = "mv {}/{} {}".format(CDR_REPO, filename, CDR_ARCHIVE)
            os.system(os_command)
        except:
            print("Error moving file {}".format(filename))
            continue


###########################################################################################################################################
def timestamp_to_date(ts):

    return datetime.datetime.fromtimestamp(ts)


###########################################################################################################################################
def date_to_timestamp(date):

    return time.mktime(datetime.datetime.strptime(date, "%Y%m%d%H%M%S").timetuple())


###########################################################################################################################################
def weekday_from_timestamp(ts):

    return datetime.datetime.fromtimestamp(ts).strftime('%a')


###########################################################################################################################################
def hour_from_timestamp(ts):

    return datetime.datetime.fromtimestamp(ts).strftime('%H')


###########################################################################################################################################
def get_cdr(start_timestamp, end_timestamp, callingNumber, calledNumber):

    conn = sqlite3.connect(CDR_DB)
    my_cursor = conn.cursor()

    if callingNumber == "*" and calledNumber == "*":
        my_select = "SELECT * from CDR where dateTimeOrigination > '{}' and dateTimeOrigination < '{}' ORDER BY dateTimeOrigination ASC".format(start_timestamp, end_timestamp)
    elif callingNumber == "*":
        my_select = "SELECT * from CDR where dateTimeOrigination > '{}' and dateTimeOrigination < '{}' and originalCalledPartyNumber = '{}' ORDER BY dateTimeOrigination ASC".format(
            start_timestamp, end_timestamp, calledNumber)
    elif calledNumber == "*":
        my_select = "SELECT * from CDR where dateTimeOrigination > '{}' and dateTimeOrigination < '{}' and callingPartyNumber = '{}' ORDER BY dateTimeOrigination ASC".format(
            start_timestamp, end_timestamp, callingNumber)
    else:
        my_select = "SELECT * from CDR where dateTimeOrigination > '{}' and dateTimeOrigination < '{}' and callingPartyNumber = '{}' and originalCalledPartyNumber = '{}' ORDER BY dateTimeOrigination ASC".format(
            start_timestamp, end_timestamp, callingNumber, calledNumber)

    my_cursor.execute(my_select)

    rows = my_cursor.fetchall()
    conn.close()

    return rows


###########################################################################################################################################
def get_cdr_record_by_callID(callID):

    conn = sqlite3.connect(CDR_DB)
    my_cursor = conn.cursor()

    my_select = "SELECT * from CDR where globalCallID_callId = '{}'".format(callID)
    my_cursor.execute(my_select)

    rows = my_cursor.fetchall()
    conn.close()

    return rows


###########################################################################################################################################
def get_cdr_by_schedule(ts, extension):

    # Main Hospital Extension -> AA
    if extension == "1001":
        if weekday_from_timestamp(ts) == "Mon" or weekday_from_timestamp(ts) == "Tue" or weekday_from_timestamp(ts) == "Wed" or weekday_from_timestamp(
                ts) == "Thu" or weekday_from_timestamp(ts) == "Fri":
            if int(hour_from_timestamp(ts)) >= 6 and int(hour_from_timestamp(ts)) < 22:
                return True

    # 1801 Clinic Hunt Pilot -> AA
    if extension == "5810":
        if weekday_from_timestamp(ts) == "Mon" or weekday_from_timestamp(ts) == "Tue" or weekday_from_timestamp(ts) == "Wed" or weekday_from_timestamp(ts) == "Thu":
            if int(hour_from_timestamp(ts)) >= 8 and int(hour_from_timestamp(ts)) < 17:
                return True
        elif weekday_from_timestamp(ts) == "Fri":
            if (int(hour_from_timestamp(ts)) >= 8 and int(hour_from_timestamp(ts)) < 12) or (int(hour_from_timestamp(ts)) >= 13 and int(hour_from_timestamp(ts)) < 16):
                return True

    # 1200 Clinic Hunt Pilot -> AA
    if extension == "5850":
        if weekday_from_timestamp(ts) == "Mon" or weekday_from_timestamp(ts) == "Tue" or weekday_from_timestamp(ts) == "Wed" or weekday_from_timestamp(ts) == "Thu":
            if (int(hour_from_timestamp(ts)) >= 8 and int(hour_from_timestamp(ts)) < 12) or (int(hour_from_timestamp(ts)) >= 13 and int(hour_from_timestamp(ts)) < 17):
                return True
        elif weekday_from_timestamp(ts) == "Fri":
            if (int(hour_from_timestamp(ts)) >= 8 and int(hour_from_timestamp(ts)) < 12):
                return True

    # Orthopedic Clinic Extension
    if extension == "7002":
        if weekday_from_timestamp(ts) == "Mon" or weekday_from_timestamp(ts) == "Tue" or weekday_from_timestamp(ts) == "Wed" or weekday_from_timestamp(ts) == "Thu":
            if (int(hour_from_timestamp(ts)) >= 8 and int(hour_from_timestamp(ts)) < 17):
                return True
        elif weekday_from_timestamp(ts) == "Fri":
            if (int(hour_from_timestamp(ts)) >= 8 and int(hour_from_timestamp(ts)) < 12):
                return True

    # Urology Clinic Extension
    if extension == "1733":
        if weekday_from_timestamp(ts) == "Mon" or weekday_from_timestamp(ts) == "Tue" or weekday_from_timestamp(ts) == "Wed" or weekday_from_timestamp(ts) == "Thu":
            if (int(hour_from_timestamp(ts)) >= 8 and int(hour_from_timestamp(ts)) < 12) or (int(hour_from_timestamp(ts)) >= 13 and int(hour_from_timestamp(ts)) < 17):
                return True
        elif weekday_from_timestamp(ts) == "Fri":
            if (int(hour_from_timestamp(ts)) >= 8 and int(hour_from_timestamp(ts)) < 12):
                return True

    # IT Helpdesk Hunt Pilot
    if extension == "3333":
        if weekday_from_timestamp(ts) == "Mon" or weekday_from_timestamp(ts) == "Tue" or weekday_from_timestamp(ts) == "Wed" or weekday_from_timestamp(
                ts) == "Thu" or weekday_from_timestamp(ts) == "Fri":
            if (int(hour_from_timestamp(ts)) >= 9 and int(hour_from_timestamp(ts)) < 17):
                return True

    return False


###########################################################################################################################################
def get_cdr_by_called_number(start_timestamp, end_timestamp, extension):

    conn = sqlite3.connect(CDR_DB)
    my_cursor = conn.cursor()

    my_select = "SELECT * from CDR where dateTimeOrigination > '{}' and dateTimeOrigination < '{}' and originalCalledPartyNumber = '{}' ORDER BY dateTimeOrigination ASC".format(
        start_timestamp, end_timestamp, extension)

    my_cursor.execute(my_select)
    rows = my_cursor.fetchall()
    conn.close()

    cdr_records = []
    for row in rows:
        if get_cdr_by_schedule(int(row[3]), extension):
            cdr_records.append(row)

    return cdr_records


###########################################################################################################################################
def count_calls_by_call_tree(my_departmentStats, cdr_records):

    for cdr_record in cdr_records:
        # print(cdr_record)
        date = datetime.datetime.fromtimestamp(int(cdr_record[3]))
        day = int(date.strftime('%d'))
        hour = int(date.strftime('%H'))

        my_departmentStats.total += 1
        my_departmentStats.total_perDay[day] += 1
        my_departmentStats.total_perHour[hour] += 1

        callID = cdr_record[0]
        callingNumber = cdr_record[4]
        calledNumber = cdr_record[5]
        finalCalledNumber = cdr_record[6]
        lastRedirectNumber = cdr_record[7]
        duration = cdr_record[8]
        origDevice = cdr_record[9]
        destDevice = cdr_record[10]

        ############################################################
        # Main Hospital Calls (this means that calledNumber is 1001) - 8307758566
        if my_departmentStats.department == "main":
            # Answered and missed from 1001
            if finalCalledNumber in ["1001", "5701", "5702", "5703", "5704", "5705"] and lastRedirectNumber == "1001":
                if duration != "0":
                    my_departmentStats.answered_1stLevel += 1
                    my_departmentStats.answered_1stLevel_perDay[day] += 1
                    my_departmentStats.answered_1stLevel_perHour[hour] += 1
                else:
                    my_departmentStats.missed_1stLevel += 1
                    my_departmentStats.missed_1stLevel_perDay[day] += 1
                    my_departmentStats.missed_1stLevel_perHour[hour] += 1
            # Answered and missed forwarded from 1001 to other extensions
            elif finalCalledNumber not in ["1001", "5701", "5702", "5703", "5704", "5705"] and lastRedirectNumber == "1001":
                if duration != "0":
                    my_departmentStats.answered_1stLevel += 1
                    my_departmentStats.answered_1stLevel_perDay[day] += 1
                    my_departmentStats.answered_1stLevel_perHour[hour] += 1
                else:
                    my_departmentStats.missed_1stLevel += 1
                    my_departmentStats.missed_1stLevel_perDay[day] += 1
                    my_departmentStats.missed_1stLevel_perHour[hour] += 1
            # Calls redirected to AA (not known in finally answered or not) - This can be further categorized
            elif finalCalledNumber == "5500" and lastRedirectNumber == "5800":
                my_departmentStats.answered_aa += 1
                my_departmentStats.answered_aa_perDay[day] += 1
                my_departmentStats.answered_aa_perHour[hour] += 1
            # Uncategorized calls (eg. calls returned to 1001 from AA - counted as answered)
            else:
                my_departmentStats.answered_1stLevel += 1
                my_departmentStats.answered_1stLevel_perDay[day] += 1
                my_departmentStats.answered_1stLevel_perHour[hour] += 1

        ##########################################################
        # 1801 Clinic Calls (this means that calledNumber is 5810) - 8307689200
        if my_departmentStats.department == "1801":
            # Answered and missed from a member of the Hunt Pilot 5810
            if finalCalledNumber == "5810" and lastRedirectNumber == "5810":
                if duration != "0":
                    my_departmentStats.answered_1stLevel += 1
                    my_departmentStats.answered_1stLevel_perDay[day] += 1
                    my_departmentStats.answered_1stLevel_perHour[hour] += 1
                else:
                    my_departmentStats.missed_1stLevel += 1
                    my_departmentStats.missed_1stLevel_perDay[day] += 1
                    my_departmentStats.missed_1stLevel_perHour[hour] += 1
            # Calls redirected to AA (not known in finally answered or not) - This can be further categorized
            elif finalCalledNumber == "5500" and lastRedirectNumber == "5811":
                my_departmentStats.answered_aa += 1
                my_departmentStats.answered_aa_perDay[day] += 1
                my_departmentStats.answered_aa_perHour[hour] += 1
            # Uncategorized calls
            else:
                my_departmentStats.answered_1stLevel += 1
                my_departmentStats.answered_1stLevel_perDay[day] += 1
                my_departmentStats.answered_1stLevel_perHour[hour] += 1

        ##########################################################
        # 1200 Clinic Calls (this means that calledNumber is 5850) - 8307742505
        if my_departmentStats.department == "1200":
            # Answered and missed from a member of the Hunt Pilot 5850
            if finalCalledNumber == "5850" and lastRedirectNumber == "5850":
                if duration != "0":
                    my_departmentStats.answered_1stLevel += 1
                    my_departmentStats.answered_1stLevel_perDay[day] += 1
                    my_departmentStats.answered_1stLevel_perHour[hour] += 1
                else:
                    my_departmentStats.missed_1stLevel += 1
                    my_departmentStats.missed_1stLevel_perDay[day] += 1
                    my_departmentStats.missed_1stLevel_perHour[hour] += 1
            # Calls redirected to AA (not known in finally answered or not) - This can be further categorized
            elif finalCalledNumber == "5500" and lastRedirectNumber == "5851":
                my_departmentStats.answered_aa += 1
                my_departmentStats.answered_aa_perDay[day] += 1
                my_departmentStats.answered_aa_perHour[hour] += 1
            # Uncategorized calls
            else:
                my_departmentStats.answered_1stLevel += 1
                my_departmentStats.answered_1stLevel_perDay[day] += 1
                my_departmentStats.answered_1stLevel_perHour[hour] += 1


###########################################################################################################################################
def count_calls_by_extension(my_extensionStats, cdr_records):

    for cdr_record in cdr_records:
        date = datetime.datetime.fromtimestamp(int(cdr_record[3]))
        day = int(date.strftime('%d'))
        hour = int(date.strftime('%H'))

        my_extensionStats.total += 1
        my_extensionStats.total_perDay[day] += 1
        my_extensionStats.total_perHour[hour] += 1

        callID = cdr_record[0]
        callingNumber = cdr_record[4]
        calledNumber = cdr_record[5]
        finalCalledNumber = cdr_record[6]
        lastRedirectNumber = cdr_record[7]
        duration = cdr_record[8]
        origDevice = cdr_record[9]
        destDevice = cdr_record[10]

        # Answered and missed calls to the corresponding extension
        if finalCalledNumber == my_extensionStats.extension and lastRedirectNumber == my_extensionStats.extension:
            if duration != "0":
                my_extensionStats.answered += 1
                my_extensionStats.answered_perDay[day] += 1
                my_extensionStats.answered_perHour[hour] += 1
            else:
                my_extensionStats.missed += 1
                my_extensionStats.missed_perDay[day] += 1
                my_extensionStats.missed_perHour[hour] += 1

        # Calls forwarded to VM
        elif finalCalledNumber == "5500" and lastRedirectNumber == my_extensionStats.extension:
            my_extensionStats.answered_vm += 1
            my_extensionStats.answered_vm_perDay[day] += 1
            my_extensionStats.answered_vm_perHour[hour] += 1

        # Calls arrives to extension by another extension
        else:
            my_extensionStats.forwarded += 1
            my_extensionStats.forwarded_perDay[day] += 1
            my_extensionStats.forwarded_perHour[hour] += 1


###########################################################################################################################################
def count_calls_by_hunt_pilot(my_huntpilotStats, cdr_records):

    for cdr_record in cdr_records:
        date = datetime.datetime.fromtimestamp(int(cdr_record[3]))
        day = int(date.strftime('%d'))
        hour = int(date.strftime('%H'))

        my_huntpilotStats.total += 1
        my_huntpilotStats.total_perDay[day] += 1
        my_huntpilotStats.total_perHour[hour] += 1

        callID = cdr_record[0]
        callingNumber = cdr_record[4]
        calledNumber = cdr_record[5]
        finalCalledNumber = cdr_record[6]
        lastRedirectNumber = cdr_record[7]
        duration = cdr_record[8]
        origDevice = cdr_record[9]
        destDevice = cdr_record[10]

        # Answered and missed calls to the corresponding extension
        if finalCalledNumber == my_huntpilotStats.huntpilot and lastRedirectNumber == my_huntpilotStats.huntpilot:
            if duration != "0":
                my_huntpilotStats.answered += 1
                my_huntpilotStats.answered_perDay[day] += 1
                my_huntpilotStats.answered_perHour[hour] += 1
            else:
                my_huntpilotStats.missed += 1
                my_huntpilotStats.missed_perDay[day] += 1
                my_huntpilotStats.missed_perHour[hour] += 1
        # Calls forwarded to VM
        elif finalCalledNumber == "5500":
            my_huntpilotStats.answered_vm += 1
            my_huntpilotStats.answered_vm_perDay[day] += 1
            my_huntpilotStats.answered_vm_perHour[hour] += 1
        elif finalCalledNumber == "3336":
            my_huntpilotStats.answered += 1
            my_huntpilotStats.answered_perDay[day] += 1
            my_huntpilotStats.answered_perHour[hour] += 1
        else:
            print(cdr_record)


###########################################################################################################################################
###########################################################################################################################################
###########################################################################################################################################
def is_cdr_date(date, clinic):
    hour = int(date.strftime('%H'))
    weekday = date.weekday()

    ### Main Hospital Business Hours
    if (clinic == "main" and (
            weekday == 0 or weekday == 1 or weekday == 2 or weekday == 3 or weekday == 4 or weekday == 5 or weekday == 6) and (hour >= 6 and hour <= 21)):
        return True

    ### 1801 Clinic Business Hours
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
    :param call_tree: the call tree (eg. main, 1801, lyndsey)
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
    elif call_tree == "1801":
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

    if is_call_tree_option(cdr_record.get_cdr_files) > -1:
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

                    # ### Further categorize CDR calls, that where answered by call-tree
                    # ### Presently it is done only for 1801
                    # if call_tree == "1801":
                    #     if categorized_call.type == "aa":
                    #         fd_tmp = open(file, "r")
                    #         found_1st_time = False
                    #         found_2nd_time = False
                    #         my_line = ""
                    #         ### Re-parse CDR file to search for AA global ID
                    #         for line_tmp in fd_tmp:
                    #             try:
                    #                 list_tmp = line_tmp.split(',')
                    #                 if list_tmp[2] == list[2] and not found_1st_time and not found_2nd_time:
                    #                     found_1st_time = True
                    #                     continue
                    #                 if list_tmp[2] == list[2] and found_1st_time and not found_2nd_time:
                    #                     found_2nd_time = True
                    #                     my_line = line_tmp
                    #                     break
                    #             except Exception as ex:
                    #                 pass
                    #         fd_tmp.close()
                    #
                    #         if found_2nd_time:
                    #             list_tmp = my_line.split(',')
                    #             cdr_record_tmp = classes.CDRRecord(list_tmp[2], datetime.datetime.fromtimestamp(int(list_tmp[4])), list_tmp[8].strip("\""),
                    #                                                list_tmp[29].strip("\""),
                    #                                                list_tmp[30].strip("\""), list_tmp[49].strip("\""),
                    #                                                list_tmp[55], list_tmp[56].strip("\""), list_tmp[57].strip("\""))
                    #             categorized_call_tmp = categorize_cdr_aa(cdr_record_tmp)
                    #
                    #             categorized_call.handle = categorized_call_tmp.handle
                    #             categorized_call.answered_by = categorized_call_tmp.answered_by
                    #             categorized_call.option = categorized_call_tmp.option
                    #             categorized_call.cdr_record_aa = categorized_call_tmp.cdr_record_aa

                except Exception as ex:
                    pass
                    # break
            fd.close()

    except Exception as ex:
        print(ex)

    return categorized_calls


###########################################################################################################################################
def count_categorized_calls(categorized_calls):
    counted_calls_daily = {'total': [0 for i in range(32)], 'answered_1st': [0 for i in range(32)], 'answered_aa': [0 for i in range(32)],
                           'missed': [0 for i in range(32)], 'missed_aa_vm': [0 for i in range(32)]}
    counted_calls_hourly = {'total': [0 for i in range(25)], 'answered_1st': [0 for i in range(25)], 'answered_aa': [0 for i in range(32)],
                            'missed': [0 for i in range(25)], 'missed_aa_vm': [0 for i in range(25)]}

    for call in categorized_calls:
        date = call.cdr_record.date
        hour = int(date.strftime('%H'))
        day = int(date.strftime('%d'))

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
def create_reports_csv(filename, report_type, counted_calls):
    # print(counted_calls['answered_1st'])
    # print(counted_calls['answered_aa'])
    # print(counted_calls['missed'])
    # print(counted_calls['missed_aa_vm'])
    # print(counted_calls['total'])

    ### Daily Reports
    if report_type == "daily":
        header = list(range(0, 33))
        header[0] = ""
        header[32] = "Total"

        # Answered 1st
        a1 = ["Answered 1st"] + counted_calls['answered_1st'][1:32] + counted_calls['answered_1st'][0:1]
        a1_tmp = list(range(0, 33))
        for i in range(32):
            try:
                a1_tmp[i] = int((counted_calls['answered_1st'][i] / counted_calls['total'][i]) * 100)
            except:
                a1_tmp[i] = 0
        a1_percent = ["Answered 1st (%)"] + a1_tmp[1:32] + a1_tmp[0:1]

        # Answered AA
        a2 = ["Answered AA"] + counted_calls['answered_aa'][1:32] + counted_calls['answered_aa'][0:1]
        a2_tmp = list(range(0, 33))
        for i in range(32):
            try:
                a2_tmp[i] = int((counted_calls['answered_aa'][i] / counted_calls['total'][i]) * 100)
            except:
                a2_tmp[i] = 0
        a2_percent = ["Answered AA(%)"] + a2_tmp[1:32] + a2_tmp[0:1]

        # Missed
        a3 = ["Missed"] + counted_calls['missed'][1:32] + counted_calls['missed'][0:1]
        a3_tmp = list(range(0, 33))
        for i in range(32):
            try:
                a3_tmp[i] = int((counted_calls['missed'][i] / counted_calls['total'][i]) * 100)
            except:
                a3_tmp[i] = 0
        a3_percent = ["Missed"] + a3_tmp[1:32] + a3_tmp[0:1]

        # Missed AA VM
        a4 = ["Missed AA VM"] + counted_calls['missed_aa_vm'][1:32] + counted_calls['missed_aa_vm'][0:1]
        a4_tmp = list(range(0, 33))
        for i in range(32):
            try:
                a4_tmp[i] = int((counted_calls['missed_aa_vm'][i] / counted_calls['total'][i]) * 100)
            except:
                a4_tmp[i] = 0
        a4_percent = ["Missed AA VM(%)"] + a4_tmp[1:32] + a4_tmp[0:1]

        a5 = ["Total"] + counted_calls['total'][1:32] + counted_calls['total'][0:1]

        print("\n")
        print(header)
        print(a1)
        print(a1_percent)
        print(a2)
        print(a2_percent)
        print(a3)
        print(a3_percent)
        print(a4)
        print(a4_percent)
        print(a5)
        print("\n")

        fd = open(filename, "w")
        csv.register_dialect('myDialect', quoting=csv.QUOTE_NONE, skipinitialspace=True)
        writer = csv.writer(fd, dialect='myDialect')
        writer.writerow(header)
        writer.writerow(a1)
        writer.writerow(a1_percent)
        writer.writerow(a2)
        writer.writerow(a2_percent)
        writer.writerow(a3)
        writer.writerow(a3_percent)
        writer.writerow(a4)
        writer.writerow(a4_percent)
        writer.writerow(a5)
        fd.close()

    ### Hourly Reports
    if report_type == "hourly":
        header = list(range(-1, 25))
        header[0] = ""
        header[25] = "Total"

        # Answered 1st
        a1 = ["Answered 1st"] + counted_calls['answered_1st'][1:25] + counted_calls['answered_1st'][0:1]
        a1_tmp = list(range(0, 26))
        for i in range(25):
            try:
                a1_tmp[i] = int((counted_calls['answered_1st'][i] / counted_calls['total'][i]) * 100)
            except:
                a1_tmp[i] = 0
        a1_percent = ["Answered 1st (%)"] + a1_tmp[1:25] + a1_tmp[0:1]

        # Answered AA
        a2 = ["Answered AA"] + counted_calls['answered_aa'][1:25] + counted_calls['answered_aa'][0:1]
        a2_tmp = list(range(0, 26))
        for i in range(25):
            try:
                a2_tmp[i] = int((counted_calls['answered_aa'][i] / counted_calls['total'][i]) * 100)
            except:
                a2_tmp[i] = 0
        a2_percent = ["Answered AA(%)"] + a2_tmp[1:25] + a2_tmp[0:1]

        # Missed
        a3 = ["Missed"] + counted_calls['missed'][1:25] + counted_calls['missed'][0:1]
        a3_tmp = list(range(0, 26))
        for i in range(25):
            try:
                a3_tmp[i] = int((counted_calls['missed'][i] / counted_calls['total'][i]) * 100)
            except:
                a3_tmp[i] = 0
        a3_percent = ["Missed"] + a3_tmp[1:25] + a3_tmp[0:1]

        # Missed AA VM
        a4 = ["Missed AA VM"] + counted_calls['missed_aa_vm'][1:25] + counted_calls['missed_aa_vm'][0:1]
        a4_tmp = list(range(0, 26))
        for i in range(25):
            try:
                a4_tmp[i] = int((counted_calls['missed_aa_vm'][i] / counted_calls['total'][i]) * 100)
            except:
                a4_tmp[i] = 0
        a4_percent = ["Missed AA VM(%)"] + a4_tmp[1:25] + a4_tmp[0:1]

        a5 = ["Total"] + counted_calls['total'][1:25] + counted_calls['total'][0:1]

        print(header)
        print(a1)
        print(a1_percent)
        print(a2)
        print(a2_percent)
        print(a3)
        print(a3_percent)
        print(a4)
        print(a4_percent)
        print(a5)

        fd = open(filename, "w")
        csv.register_dialect('myDialect', quoting=csv.QUOTE_NONE, skipinitialspace=True)
        writer = csv.writer(fd, dialect='myDialect')
        writer.writerow(header)
        writer.writerow(a1)
        writer.writerow(a1_percent)
        writer.writerow(a2)
        writer.writerow(a2_percent)
        writer.writerow(a3)
        writer.writerow(a3_percent)
        writer.writerow(a4)
        writer.writerow(a4_percent)
        writer.writerow(a5)
        fd.close()


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
    TIMEZONE = +5  # Time shift from GMT (which is the default for CDR filenames)

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
