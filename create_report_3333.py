import json
import datetime
import os
from pathlib import Path

import send_mail

####################################################################################################
# CDR filename is in UTC. Timestamps inside CDR files are in client's CUCM timezone.

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


####################################################################################################
# MAIN #
start = datetime.datetime.now()
CDR_FOLDER = 'cdr_data\\'                           # Windows
DATA_FOLDER = 'data\\'

# CDR_FOLDER = '/home/cdr/cdr_data/'                # Linux
# CDR_FILENAME = 'data/cdr-3333.txt'

CDR_FILENAMES = [DATA_FOLDER + fn for fn in \
                     ['cdr-3333-total.txt', 'cdr-3333-voicemail.txt', 'cdr-3333-unanswered.txt', \
                      'cdr-calls-3691.txt', 'cdr-calls-3334.txt', 'cdr-calls-3730.txt', \
                      'cdr-calls-2547.txt', 'cdr-calls-3686.txt']]
print(CDR_FILENAMES)

# Initialize Variables
calls_voicemail = 0
calls_unanswered = 0
calls_answered = {'total': 0, '3891': 0, '3334': 0, '3730': 0, '2547': 0, '3686': 0}

fd = []
for CDR in CDR_FILENAMES:
    fd.append(open(CDR, "w"))

# List directory files only with CDR files
cdr_file_list=[]
for filename in os.listdir(CDR_FOLDER):
    if filename.startswith("cdr_Stand"):
        cdr_file_list.append(filename)
# print(cdr_file_list)

# Parse CDR file
try:
    for file in cdr_file_list:
        file_descriptor = open(CDR_FOLDER+file, "r")
        for line in file_descriptor:
            try:
                list = line.split(',')
                date = datetime.datetime.fromtimestamp(int(list[4]))
                # day = int(date.strftime('%d'))
                # hour = int(date.strftime('%H'))
                # print(list)
                if (list[29]) == "\"3333\"":
                    # print("\n---\n",date, list[8], list[29], list[30], list[49], list[55], list[57])
                    # temp = ' '.join([str(date), list[8], list[29], list[30], list[49], list[55], list[57], "\n"])
                    temp = ' '.join([str(date), list[8], list[55], "\n"])
                    fd[0].write(temp)
                    if(list[30]) == "\"5500\"":
                        calls_voicemail += 1
                        temp = ' '.join([str(date), list[8], list[55], "\n"])
                        fd[1].write(temp)
                    elif (list[30]) == "\"3333\"" and list[55] is "0":
                        calls_unanswered += 1
                        temp = ' '.join([str(date), list[8], list[55], "\n"])
                        fd[2].write(temp)
                    else:
                        # print("\n---\n",date, list[8], list[29], list[30], list[49], list[55], list[57])
                        calls_answered['total'] += 1
                        if(list[57] == '"SEPBC16F516B359"'):
                            temp = ' '.join([str(date), list[8], list[55], "\n"])
                            fd[3].write(temp)
                            calls_answered['3891'] += 1
                        elif(list[57] == '"SEP34A84EA6A74E"'):
                            temp = ' '.join([str(date), list[8], list[55], "\n"])
                            fd[4].write(temp)
                            calls_answered['3334'] += 1
                        elif(list[57] == '"SEPBC16F516D030"'):
                            temp = ' '.join([str(date), list[8], list[55], "\n"])
                            fd[5].write(temp)
                            calls_answered['3730'] += 1
                        elif(list[57] == '"SEP7426AC635AAF"'):
                            temp = ' '.join([str(date), list[8], list[55], "\n"])
                            fd[6].write(temp)
                            calls_answered['2547'] += 1
                        elif (list[57] in ['"SEPBC16F516CDD2"', '"CSF3686"']):
                            temp = ' '.join([str(date), list[8], list[55], "\n"])
                            fd[7].write(temp)
                            calls_answered['3686'] += 1
                        else:
                            print(list[57])
            except Exception as ex:
                # print(ex)
                continue


    print("calls_voicemail = ",calls_voicemail)
    print("calls_unanswered = ",calls_unanswered)
    print("calls_answered = ",calls_answered)
    calls_total = calls_answered['total'] + calls_voicemail + calls_unanswered
    print("calls_total = ", calls_total)

    for f in fd:
        f.close()

except Exception as ex:
    print(ex)


####################################################################################################
# Prepare report and send e-mail
subject = "Weekly Report for x3333 (9am - 5pm)"
# attachments = ['data/cdr-3333.txt']
attachments = []

access = json.load(open('data/access.json'))
USERNAME = str(access["gmail"]["username"])
PASSWORD = str(access["gmail"]["password"])
#calls_answered = {'total': 0, '3891': 0, '3334': 0, '3730': 0, '2547': 0, '3686': 0}

body = """
Total calls to x3333: {}<br>
---------------------------------<br>
Calls answered by Human: {}<br>
Calls answered by Voicemail: {}<br>
Calls not answered: {}<br>
---------------------------------<br>
Call answered by Jimmy DeAnda (x3891): {}<br>
Call answered by Gilbert Tovar (x3334): {}<br>
Call answered by ??? (x3730): {}<br>
Call answered by ??? (x2547): {}<br>
Call answered by Albert Lattimer (x3686): {}<br>
---------------------------------<br>
""".format(calls_total, calls_answered['total'], calls_voicemail, calls_unanswered, calls_answered['3891'], calls_answered['3334'], calls_answered['3730'], \
           calls_answered['2547'], calls_answered['3686'])

print(body)

toaddr = ['georgios.fotiadis@gmail.com']
send_mail.send_mail(USERNAME, PASSWORD, toaddr, subject, body, CDR_FILENAMES)


# Measure Script Execution
print("\n\nRutime = ",datetime.datetime.now()-start)
