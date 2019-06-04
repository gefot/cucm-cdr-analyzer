import datetime
import time

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

STARTDATE = "201906040000"
ENDDATE = "201906050000"
# EXTENSION_LIST = ["5810", "5811", "5500"]
# EXTENSION_LIST = ["*"]
EXTENSION_LIST = ["5122290591"]

cdr_file_list = module_funcs.get_cdr_files(STARTDATE, ENDDATE)

# Parse CDR file
try:
    for file in cdr_file_list:
        # print("\n\n\n {}".format(file))
        fd = open(file, "r")
        for line in fd:
            try:
                list = line.split(',')
                for extension in EXTENSION_LIST:
                    if extension == "*":
                        date = datetime.datetime.fromtimestamp(int(list[4]))
                        print(list[2], date, list[8], list[29], list[30], list[49], time.strftime("%M:%S", time.gmtime(int(int(list[55])))), list[56], list[57])
                        break
                    elif list[8] == "\"" + extension + "\"" or list[29] == "\"" + extension + "\"":
                        date = datetime.datetime.fromtimestamp(int(list[4]))
                        print(list[2], date, list[8], list[29], list[30], list[49], time.strftime("%M:%S", time.gmtime(int(int(list[55])))), list[56], list[57])
            except Exception as ex:
                pass
                # break
        fd.close()

except Exception as ex:
    print(ex)
