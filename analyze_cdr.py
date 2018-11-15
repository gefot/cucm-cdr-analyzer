import json
import os
import datetime
import time
import _module_funcs

access = json.load(open('access.json'))                            # Windows
SRC_FOLDER = '/home/cdr/cdr_data/'
DST_FOLDER = 'ftp_files/'

# access = json.load(open('/home/pbx/cucm-cdr-analyzer/access.json'))  # Linux
# SRC_FOLDER = '/home/cdr/cdr_data/'
# DST_FOLDER = '/home/pbx/cucm-cdr-analyzer/ftp_files/'

PATTTERN = '2018111513'
SERVER = str(access["ftp"]["server"])
USERNAME = str(access["ftp"]["username"])
PASSWORD = str(access["ftp"]["password"])


_module_funcs.get_files_ftp(SERVER, USERNAME, PASSWORD, SRC_FOLDER, DST_FOLDER, PATTTERN)

cdr_file_list=[]
for filename in os.listdir(DST_FOLDER):
    cdr_file_list.append(filename)
cdr_file_list.sort()
print(cdr_file_list)
print("len = ",len(cdr_file_list))

# Parse CDR file
try:
    for file in cdr_file_list:
        fd = open(DST_FOLDER+file, "r")
        for line in fd:
            try:
                list = line.split(',')
                date = datetime.datetime.fromtimestamp(int(list[4]))
                print(date, list[8], list[29], list[30], list[49], time.strftime("%M:%S", time.gmtime(int(int(list[55])))), list[57])
            except Exception as ex:
                pass
except Exception as ex:
    print(ex)

