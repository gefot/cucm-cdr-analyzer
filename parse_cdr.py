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

CDR_CURRENT = '/home/gfot/cdr/cdr_data/'
EXTENSION = "\"4208\""
STARTDATE = "201906291200"
ENDDATE = "201906291500"
TIMEZONE = +5

now = datetime.datetime.now()
nowdate = now.strftime("%Y%m")
print(nowdate)

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

# Construct CDR folder
cdr_folder = []
if nowdate in startdate_new or nowdate in enddate_new:
    cdr_folder.append(CDR_CURRENT)

print("CDR_FOLDER = {}".format(cdr_folder))

# Get CDR files according to start and end dates
cdr_file_list = []
for my_folder in cdr_folder:
    for filename in os.listdir(my_folder):
        if filename.startswith("cdr") and "_01_" in filename:
            cdr_pattern = re.search(r'cdr_\w*_\d\d_(\d\d\d\d\d\d\d\d\d\d\d\d)', filename).group(1)
            if int(cdr_pattern) > int(startdate_new) and int(cdr_pattern) < int(enddate_new):
                cdr_file_list.append(cdr_folder + filename)
cdr_file_list.sort()
print(cdr_file_list)
print("len = ", len(cdr_file_list))

# Parse CDR file
try:
    for file in cdr_file_list:
        # print("\n\n\n {}".format(file))
        fd = open(file, "r")
        for line in fd:
            try:
                list = line.split(',')
                # if list[8] == EXTENSION or list[29] == EXTENSION:
                if 1 == 1:
                    date = datetime.datetime.fromtimestamp(int(list[4]))
                    print(list[2], date, list[8], list[29], list[30], list[49],
                          time.strftime("%M:%S", time.gmtime(int(int(list[55])))), list[56], list[57])
            except Exception as ex:
                pass
        # break
except Exception as ex:
    print(ex)
