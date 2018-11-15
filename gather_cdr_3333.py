import datetime
import os
from pathlib import Path

####################################################################################################
# MAIN #

# CDR_SRC_FOLDER = 'cdr_data\\'               # Windows
# CDR_DST_FOLDER = 'cdr_data_3333\\'

CDR_SRC_FOLDER = '/home/cdr/cdr_data/'        # Linux
CDR_DST_FOLDER = '/home/cdr/cdr_data_3333/'

date = datetime.datetime.now()
prev_dates = [date + datetime.timedelta(days=-i) for i in range(1,5)]
prev_cdr_dates = [date.strftime('%Y')+date.strftime('%m')+date.strftime('%d') for date in prev_dates]
# print("prev_dates = ", prev_dates)
print("prev_cdr_dates = ", prev_cdr_dates)

# Append to the previous 4 days the hour, which is in CST-6. Working hours for 3333 are 9am-5pm.
cdr_filenames = []
for date in prev_cdr_dates:
    cdr_filenames.append(date + "15")
    cdr_filenames.append(date + "16")
    cdr_filenames.append(date + "17")
    cdr_filenames.append(date + "18")
    cdr_filenames.append(date + "19")
    cdr_filenames.append(date + "20")
    cdr_filenames.append(date + "21")
    cdr_filenames.append(date + "22")
# print(cdr_filenames)

# List directory files only with CDR files of interest
cdr_file_list = []
for filename in os.listdir(CDR_SRC_FOLDER):
    if filename.startswith("cdr"):
        for cdr in cdr_filenames:
            if cdr in filename:
                cdr_file_list.append(filename)

print("\n")
# print(os.listdir(CDR_SRC_FOLDER))
print("len = ", len(os.listdir(CDR_SRC_FOLDER)))
# print(cdr_file_list)
print("len = ", len(cdr_file_list))

command = 'rm -rf ' + CDR_DST_FOLDER + '*'
os.system(command)
for a in cdr_file_list:
    command = 'cp ' + CDR_SRC_FOLDER+a + ' ' + CDR_DST_FOLDER+a
    os.system(command)

