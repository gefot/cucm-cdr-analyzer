import datetime
import os
from pathlib import Path

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
# CDR_FOLDER= str(Path(__file__).parent) + '\cdr_data\\'      # Windows
# CDR_FILENAME = 'data\\cdr-3333.txt'

CDR_FOLDER = '/home/cdr/cdr_data/'                        # Linux
CDR_FILENAME = 'data/cdr-3333.txt'

# List directory files only with CDR files
cdr_file_list=[]
for filename in os.listdir(CDR_FOLDER):
    if filename.startswith("cdr_Stand"):
        cdr_file_list.append(filename)
# print(cdr_file_list)

# Initialize Variables
calls_voicemail = 0
calls_unanswered = 0
calls_answered = {'total': 0, '3891': 0, '3334': 0, '3730': 0, '2547': 0, '3686': 0}

# Parse CDR file
fd1 = open(CDR_FILENAME, "w")
try:
    for file in cdr_file_list:
        fd = open(CDR_FOLDER+file, "r")
        for line in fd:
            try:
                list = line.split(',')
                date = datetime.datetime.fromtimestamp(int(list[4]))
                # day = int(date.strftime('%d'))
                # hour = int(date.strftime('%H'))
                # print(list)
                if (list[29]) == "\"3333\"":
                    # print("\n---\n",date, list[8], list[29], list[30], list[49], list[55], list[57])
                    temp = ' '.join([str(date), list[8], list[29], list[30], list[49], list[55], list[57], "\n"])
                    fd1.write(temp)
                    if(list[30]) == "\"5500\"":
                        calls_voicemail += 1
                    elif (list[30]) == "\"3333\"" and list[55] is "0":
                        calls_unanswered += 1
                    else:
                        # print("\n---\n",date, list[8], list[29], list[30], list[49], list[55], list[57])
                        calls_answered['total'] += 1
                        if(list[57] == '"SEPBC16F516B359"'):
                            calls_answered['3891'] += 1
                        elif(list[57] == '"SEP34A84EA6A74E"'):
                            calls_answered['3334'] += 1
                        elif(list[57] == '"SEPBC16F516D030"'):
                            calls_answered['3730'] += 1
                        elif(list[57] == '"SEP7426AC635AAF"'):
                            calls_answered['2547'] += 1
                        elif (list[57] in ['"SEPBC16F516CDD2"', '"CSF3686"']):
                            calls_answered['3686'] += 1
                        else:
                            print(list[57])
            except Exception as ex:
                # print(ex)
                continue

    print("calls_voicemail = ",calls_voicemail)
    print("calls_unanswered = ",calls_unanswered)
    print("calls_answered = ",calls_answered)

except Exception as ex:
    print(ex)

# Measure Script Execution
print("\n\nRutime = ",datetime.datetime.now()-start)

