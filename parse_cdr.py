import json
import os
import datetime
import re
import time
import pytz
import module_funcs

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

CDR_FOLDER = '/home/gfot/cdr/cdr_data/'
EXTENSION = "\"4208\""
STARTDATE = "201905291200"
ENDDATE = "201905291500"
TIMEZONE = +5

# Get files from FTP server
# access = json.load(open('/home/gfot/cucm-cdr-analyzer/data/access.json'))  # Linux
# SERVER = str(access["ftp"]["server"])
# USERNAME = str(access["ftp"]["username"])
# PASSWORD = str(access["ftp"]["password"])
# DST_FOLDER = '/home/gfot/cucm-cdr-analyzer/data/ftp_files/'
# module_funcs.get_files_ftp(SERVER, USERNAME, PASSWORD, CDR_FOLDER, DST_FOLDER, PATTTERN)


# Shift dates to GMT so as to much CDR
print("local time = ", STARTDATE)
startdate_obj = datetime.datetime.strptime(STARTDATE, '%Y%m%d%H%M')
startdate_obj_new = startdate_obj + datetime.timedelta(hours=TIMEZONE)
startdate_new = datetime.datetime.strftime(startdate_obj_new, '%Y%m%d%H%M')
print("GMT time = ", startdate_new)

print("local time = ", ENDDATE)
enddate_obj = datetime.datetime.strptime(ENDDATE, '%Y%m%d%H%M')
enddate_obj_new = enddate_obj + datetime.timedelta(hours=TIMEZONE)
enddate_new = datetime.datetime.strftime(enddate_obj_new, '%Y%m%d%H%M')
print("GMT time = ", enddate_new)

# Get CDR files according to start and end dates
cdr_file_list = []
for filename in os.listdir(CDR_FOLDER):
    if filename.startswith("cdr") and "_01_" in filename:
        cdr_pattern = re.search(r'cdr_\w*_\d\d_(\d\d\d\d\d\d\d\d\d\d\d\d)', filename).group(1)
        if int(cdr_pattern) > int(startdate_new) and int(cdr_pattern) < int(enddate_new):
            cdr_file_list.append(filename)
cdr_file_list.sort()
print(cdr_file_list)
print("len = ", len(cdr_file_list))

# Parse CDR file
try:
    for file in cdr_file_list:
        # print("\n\n\n {}".format(file))
        fd = open(CDR_FOLDER + file, "r")
        for line in fd:
            try:
                list = line.split(',')
                if list[8] == EXTENSION or list[29] == EXTENSION:
                    date = datetime.datetime.fromtimestamp(int(list[4]))
                    print(list[2], date, list[8], list[29], list[30], list[49],
                          time.strftime("%M:%S", time.gmtime(int(int(list[55])))), list[56], list[57])
            except Exception as ex:
                pass
        # break
except Exception as ex:
    print(ex)
