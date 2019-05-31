import datetime
import os
from pathlib import Path

####################################################################################################
# MAIN #

CDR_SRC_FOLDER = '/home/gfot/cdr/cdr_data/'        # Linux
CDR_DST_FOLDER = '/home/gfot/cdr/cdr_data_daily/'

date = datetime.datetime.now()
# date = datetime.datetime.now() + datetime.timedelta(days=-1)
cur_date = date.strftime('%Y') + date.strftime('%m') + date.strftime('%d')
next = date + datetime.timedelta(days=1)
next_date = next.strftime('%Y') + next.strftime('%m') + next.strftime('%d')

# Append to the previous 4 days the hour, which is in CST-6.
cdr_filenames = []
# for date in prev_cdr_dates:
cdr_filenames.append(cur_date + "12")
cdr_filenames.append(cur_date + "13")
cdr_filenames.append(cur_date + "14")
cdr_filenames.append(cur_date + "15")
cdr_filenames.append(cur_date + "16")
cdr_filenames.append(cur_date + "17")
cdr_filenames.append(cur_date + "18")
cdr_filenames.append(cur_date + "19")
cdr_filenames.append(cur_date + "20")
cdr_filenames.append(cur_date + "21")
cdr_filenames.append(cur_date + "22")
cdr_filenames.append(cur_date + "23")
cdr_filenames.append(next_date + "00")
cdr_filenames.append(next_date + "01")
cdr_filenames.append(next_date + "02")
cdr_filenames.append(next_date + "03")
cdr_filenames.append(next_date + "04")
print(cdr_filenames)

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

