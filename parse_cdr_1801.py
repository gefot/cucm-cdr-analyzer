import datetime
import time

import module_funcs
import classes

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

STARTDATE = "201906040900"
ENDDATE =   "201906041100"

cdr_file_list = module_funcs.get_cdr_files(STARTDATE, ENDDATE)

# Parse CDR file
try:
    for file in cdr_file_list:
        # print("\n\n\n {}".format(file))
        fd = open(file, "r")
        for line in fd:
            try:
                list = line.split(',')

                global_id = list[2]
                date = datetime.datetime.fromtimestamp(int(list[4]))
                calling_num = list[8].strip("\"")
                called_num = list[29].strip("\"")
                final_called_num = list[30].strip("\"")
                last_redirect_num = list[49].strip("\"")
                duration = time.strftime("%M:%S", time.gmtime(int(int(list[55]))))
                origDeviceName = list[56].strip("\"")
                destDeviceName = list[57].strip("\"")

                cdr_record = classes.CDRRecord(global_id, date, calling_num, called_num, final_called_num, last_redirect_num, duration, origDeviceName, destDeviceName)
                print(cdr_record)

            except Exception as ex:
                # Catch exception for file headers
                # print("Error parsing: {}".format(line))
                pass
                # break
        fd.close()

except Exception as ex:
    print(ex)

