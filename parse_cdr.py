import json
import os
import datetime
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

access = json.load(open('data/access.json'))                                # Windows
SRC_FOLDER = '/home/cdr/cdr_data/'
DST_FOLDER = 'data/ftp_files/'

# access = json.load(open('/home/pbx/cucm-cdr-analyzer/data/access.json'))  # Linux
# SRC_FOLDER = '/home/cdr/cdr_data/'
# DST_FOLDER = '/home/pbx/cucm-cdr-analyzer/data/ftp_files/'


PATTTERN = 'cdr_\w*_\d\d_2018120318'
SERVER = str(access["ftp"]["server"])
USERNAME = str(access["ftp"]["username"])
PASSWORD = str(access["ftp"]["password"])

# # Get files from FTP server
module_funcs.get_files_ftp(SERVER, USERNAME, PASSWORD, SRC_FOLDER, DST_FOLDER, PATTTERN)

cdr_file_list=[]
for filename in os.listdir(DST_FOLDER):
    if filename.startswith("cdr") and "_01_" in filename:
        cdr_file_list.append(filename)
cdr_file_list.sort()
print(cdr_file_list)
print("len = ",len(cdr_file_list))

# Parse CDR file
try:
    for file in cdr_file_list:
        print("\n\n\n {}".format(file))
        fd = open(DST_FOLDER+file, "r")
        for line in fd:
            try:
                list = line.split(',')
                date = datetime.datetime.fromtimestamp(int(list[4]))
                print(date, list[2], list[8], list[29], list[30], list[49], time.strftime("%M:%S", time.gmtime(int(int(list[55])))), list[57])
            except Exception as ex:
                pass
        # break
except Exception as ex:
    print(ex)

