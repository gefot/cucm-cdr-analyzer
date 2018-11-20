
import json
import os
import time, datetime
import glob

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


# access = json.load(open('data\\access.json'))                               # Windows
# CDR_FOLDER = "E:\\PyCharmProjects\\cucm-cdr-analyzer\\data\\cdr_data\\"

access = json.load(open('/home/pbx/cucm-cdr-analyzer/data/access.json'))  # Linux
CDR_FOLDER = "/home/cdr/cdr_data/"      # Linux

date = datetime.datetime.now()
today = date.strftime('%Y')+date.strftime('%m')+date.strftime('%d')
# today = "20181119"
# print(today)

# os.chdir(CDR_FOLDER)        # Windows
# files = glob.glob("cdr*")   # Windows
files = glob.glob(CDR_FOLDER+"cdr*_01_*{}*".format(today))     # Linux

# print(files)
newest = max(files, key = os.path.getctime)
print(newest)

body = ""
fd = open(newest, "r")
for line in fd:
    try:
        list = line.split(',')
        #print(list)
        print(date, list[2], list[8], list[29], list[30], list[49], time.strftime("%M:%S", time.gmtime(int(int(list[55])))), list[57])
        if list[29] == "\"3556\"":
            date = datetime.datetime.fromtimestamp(int(list[4]))
            temp =  list[8].replace("\"","") + " dialed 911 at " + str(date) + "<br>"
            body += temp
    except Exception as ex:
        pass

print(body)
subject = "911 Report"
attachments = []
USERNAME = str(access["gmail"]["username"])
PASSWORD = str(access["gmail"]["password"])
toaddr = ["georgios.fotiadis@gmail.com"]
module_funcs.send_mail(USERNAME, PASSWORD, toaddr, subject, body, attachments)