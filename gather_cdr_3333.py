import datetime
import time
import os
from pathlib import Path

####################################################################################################
# MAIN #
# CDR_SRC_FOLDER = 'cdr_data\\'                   # Windows
# CDR_DST_FOLDER = 'cdr_data_3333\\'              # Windows

CDR_SRC_FOLDER = '/home/cdr/cdr_data/'        # Linux
CDR_DST_FOLDER = '/home/cdr/cdr_data_3333/'   # Linux

date = datetime.datetime.now()
prev_dates = [date + datetime.timedelta(days=-i) for i in range(1,5)]
prev_cdr_dates = [date.strftime('%Y')+date.strftime('%m')+date.strftime('%d') for date in prev_dates]
# print("prev_dates = ", prev_dates)
print("prev_cdr_dates = ", prev_cdr_dates)

# timezone = int(time.timezone / -(60*60))
# utc_date = date + datetime.timedelta(hours=-timezone)
# print("utc_date = ", utc_date)

# Append to the previous 4 days the hour, which is in CST-6. Working hours for 3333 are 9am-5pm.
cdr_filenames = []
for date in prev_cdr_dates:
    cdr_filenames.append(date + "03")
    cdr_filenames.append(date + "04")
    cdr_filenames.append(date + "05")
    cdr_filenames.append(date + "06")
    cdr_filenames.append(date + "07")
    cdr_filenames.append(date + "08")
    cdr_filenames.append(date + "09")
    cdr_filenames.append(date + "10")
# print(cdr_filenames)

# List directory files only with CDR files of interest
cdr_file_list = []
for filename in os.listdir(CDR_SRC_FOLDER):
    if filename.startswith("cdr"):
        for cdr in cdr_filenames:
            if cdr in filename:
                cdr_file_list.append(filename)
print("\n")
print(os.listdir(CDR_SRC_FOLDER))
print("len = ", len(os.listdir(CDR_SRC_FOLDER)))
print(cdr_file_list)
print("len = ", len(cdr_file_list))

command = 'rm ' + CDR_DST_FOLDER + '*'
os.system(command)
for a in cdr_file_list:
    command = 'cp ' + CDR_SRC_FOLDER+a + ' ' + CDR_DST_FOLDER+a
    os.system(command)

