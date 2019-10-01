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

CDR_REPO = '/home/gfot/cdr/cdr_repo/'
CDR_ARCHIVE = '/home/gfot/cdr/cdr_archive/'
CDR_DB = "/home/gfot/cucm-cdr-analyzer/cucm.db"
VM_PILOT = "5500"


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
def timestamp_to_date(my_timestamp):
    return datetime.datetime.fromtimestamp(my_timestamp)


###########################################################################################################################################
def date_to_timestamp(my_date):
    return time.mktime(datetime.datetime.strptime(my_date, "%Y%m%d%H%M%S").timetuple())


###########################################################################################################################################
def weekday_from_timestamp(my_timestamp):
    return datetime.datetime.fromtimestamp(my_timestamp).strftime('%a')


###########################################################################################################################################
def hour_from_timestamp(my_timestamp):
    return datetime.datetime.fromtimestamp(my_timestamp).strftime('%H')


###########################################################################################################################################
def week_timestamp_range_from_date(my_date):
    dt = datetime.datetime.strptime(my_date, '%Y%m%d%H%M%S')

    start = dt - datetime.timedelta(days=dt.weekday())
    end = start + datetime.timedelta(days=6)

    my_start = start.replace(hour=0, minute=1, second=0).strftime('%Y%m%d%H%M%S')
    my_end = end.replace(hour=23, minute=59, second=0).strftime('%Y%m%d%H%M%S')
    print("inside week_timestamp_range_from_date: ", my_start, my_end)
    week_range = [date_to_timestamp(my_start), date_to_timestamp(my_end)]
    # print(week_range)

    return week_range


###########################################################################################################################################
def day_timestamp_range_from_date(my_date):
    dt = datetime.datetime.strptime(my_date, '%Y%m%d%H%M%S')

    my_start = dt.replace(hour=0, minute=1, second=0).strftime('%Y%m%d%H%M%S')
    my_end = dt.replace(hour=23, minute=59, second=0).strftime('%Y%m%d%H%M%S')
    print(my_start, my_end)
    day_range = [date_to_timestamp(my_start), date_to_timestamp(my_end)]
    # print(day_range)

    return day_range


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

        finalCalledNumber = cdr_record[6]
        lastRedirectNumber = cdr_record[7]
        duration = cdr_record[8]

        my_departmentStats.total += 1
        my_departmentStats.total_perDay[day] += 1
        my_departmentStats.total_perHour[hour] += 1

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
            elif finalCalledNumber == VM_PILOT and lastRedirectNumber == "5800":
                my_departmentStats.answered_aa += 1
                my_departmentStats.answered_aa_perDay[day] += 1
                my_departmentStats.answered_aa_perHour[hour] += 1
            # Uncategorized calls (eg. calls returned to 1001 from AA - counted as answered)
            else:
                my_departmentStats.answered_1stLevel += 1
                my_departmentStats.answered_1stLevel_perDay[day] += 1
                my_departmentStats.answered_1stLevel_perHour[hour] += 1

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
            elif finalCalledNumber == VM_PILOT and lastRedirectNumber == "5811":
                my_departmentStats.answered_aa += 1
                my_departmentStats.answered_aa_perDay[day] += 1
                my_departmentStats.answered_aa_perHour[hour] += 1
            # Uncategorized calls
            else:
                my_departmentStats.answered_1stLevel += 1
                my_departmentStats.answered_1stLevel_perDay[day] += 1
                my_departmentStats.answered_1stLevel_perHour[hour] += 1

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
            elif finalCalledNumber == VM_PILOT and lastRedirectNumber == "5851":
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

        finalCalledNumber = cdr_record[6]
        lastRedirectNumber = cdr_record[7]
        duration = cdr_record[8]

        my_extensionStats.total += 1
        my_extensionStats.total_perDay[day] += 1
        my_extensionStats.total_perHour[hour] += 1

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
        elif finalCalledNumber == VM_PILOT and lastRedirectNumber == my_extensionStats.extension:
            my_extensionStats.answered_vm += 1
            my_extensionStats.answered_vm_perDay[day] += 1
            my_extensionStats.answered_vm_perHour[hour] += 1

        # Calls arrived to extension by another extension
        elif finalCalledNumber == my_extensionStats.extension and lastRedirectNumber != my_extensionStats.extension:
            if duration != "0":
                my_extensionStats.answered += 1
                my_extensionStats.answered_perDay[day] += 1
                my_extensionStats.answered_perHour[hour] += 1
            else:
                my_extensionStats.missed += 1
                my_extensionStats.missed_perDay[day] += 1
                my_extensionStats.missed_perHour[hour] += 1

        # Misc calls that should not be accounted for - can be excluded
        else:
            my_extensionStats.total -= 1
            my_extensionStats.total_perDay[day] -= 1
            my_extensionStats.total_perHour[hour] -= 1


###########################################################################################################################################
def count_calls_by_hunt_pilot(my_huntpilotStats, cdr_records):
    for cdr_record in cdr_records:
        date = datetime.datetime.fromtimestamp(int(cdr_record[3]))
        day = int(date.strftime('%d'))
        hour = int(date.strftime('%H'))

        finalCalledNumber = cdr_record[6]
        lastRedirectNumber = cdr_record[7]
        duration = cdr_record[8]
        destDevice = cdr_record[10]

        my_huntpilotStats.total += 1
        my_huntpilotStats.total_perDay[day] += 1
        my_huntpilotStats.total_perHour[hour] += 1

        # Answered and missed calls to the corresponding extension
        if finalCalledNumber == my_huntpilotStats.huntpilot and lastRedirectNumber == my_huntpilotStats.huntpilot:
            if duration != "0":
                my_huntpilotStats.answered += 1
                my_huntpilotStats.answered_perDay[day] += 1
                my_huntpilotStats.answered_perHour[hour] += 1
                try:
                    my_huntpilotStats.answeredBy[destDevice] += 1
                except:
                    my_huntpilotStats.answeredBy[destDevice] = 1
            else:
                my_huntpilotStats.missed += 1
                my_huntpilotStats.missed_perDay[day] += 1
                my_huntpilotStats.missed_perHour[hour] += 1

        # Calls forwarded to VM
        elif finalCalledNumber == VM_PILOT:
            my_huntpilotStats.answered_vm += 1
            my_huntpilotStats.answered_vm_perDay[day] += 1
            my_huntpilotStats.answered_vm_perHour[hour] += 1

        # Calls not answered by hunt pilot, but forwarded to somewhere else (eg Fwd Noan)...
        elif finalCalledNumber != my_huntpilotStats.huntpilot and lastRedirectNumber == my_huntpilotStats.huntpilot:
            # Calls queued (if native call queueing is used) - can be excluded
            if destDevice == "ParkingLotDDevice":
                my_huntpilotStats.total -= 1
                my_huntpilotStats.total_perDay[day] -= 1
                my_huntpilotStats.total_perHour[hour] -= 1
            else:
                if duration != "0":
                    my_huntpilotStats.answered += 1
                    my_huntpilotStats.answered_perDay[day] += 1
                    my_huntpilotStats.answered_perHour[hour] += 1
                    try:
                        my_huntpilotStats.answeredBy[destDevice] += 1
                    except:
                        my_huntpilotStats.answeredBy[destDevice] = 1
                else:
                    my_huntpilotStats.missed += 1
                    my_huntpilotStats.missed_perDay[day] += 1
                    my_huntpilotStats.missed_perHour[hour] += 1

        # Misc calls that should not be accounted for - can be excluded
        else:
            my_huntpilotStats.total -= 1
            my_huntpilotStats.total_perDay[day] -= 1
            my_huntpilotStats.total_perHour[hour] -= 1

###########################################################################################################################################
