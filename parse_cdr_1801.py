
import datetime

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

STARTDATE = "201906030900"
ENDDATE = "201906041600"

cdr_file_list = module_funcs.get_cdr_files(STARTDATE, ENDDATE)

# Parse CDR file
categorized_calls = []
try:
    for file in cdr_file_list:
        # print("\n\n\n {}".format(file))
        fd = open(file, "r")
        for line in fd:
            try:
                list = line.split(',')
                cdr_record = classes.CDRRecord(list[2], datetime.datetime.fromtimestamp(int(list[4])), list[8].strip("\""), list[29].strip("\""),
                                               list[30].strip("\""), list[49].strip("\""),
                                               list[55], list[56].strip("\""), list[57].strip("\""))
                categorized_call = module_funcs.categorize_cdr(cdr_record)
                if categorized_call != {}:
                    categorized_call['cdr_record'] = cdr_record
                    categorized_call['cdr_record_aa'] = ""
                    # print("categorized_call = {}".format(categorized_call))
                    categorized_calls.append(categorized_call)

                # Further categorize CDR calls
                if categorized_call['type'] == "aa":
                    # print("\nFound an AA call!!")
                    # print(cdr_record)

                    fd_tmp = open(file, "r")
                    found_1st = False
                    found_2nd = False
                    my_line = ""
                    for line_tmp in fd_tmp:
                        try:
                            list_tmp = line_tmp.split(',')
                            if list_tmp[2] == list[2] and not found_1st and not found_2nd:
                                found_1st = True
                                continue
                            if list_tmp[2] == list[2] and found_1st and not found_2nd:
                                found_2nd = True
                                my_line = line_tmp
                                break
                        except Exception as ex:
                            pass
                    fd_tmp.close()

                    if found_2nd:
                        # print("my_line = {}".format(my_line))
                        list_tmp = my_line.split(',')
                        cdr_record_tmp = classes.CDRRecord(list_tmp[2], datetime.datetime.fromtimestamp(int(list_tmp[4])), list_tmp[8].strip("\""), list_tmp[29].strip("\""),
                                                           list_tmp[30].strip("\""), list_tmp[49].strip("\""),
                                                           list_tmp[55], list_tmp[56].strip("\""), list_tmp[57].strip("\""))
                        categorized_call_tmp = module_funcs.categorize_cdr_aa(cdr_record_tmp)
                        # print(cdr_record_tmp)
                        # print(categorized_call_tmp)

                        categorized_call = dict(categorized_call_tmp)
                        categorized_call['cdr_record_aa'] = cdr_record_tmp

            except Exception as ex:
                pass
                # break
        fd.close()

except Exception as ex:
    print(ex)


print("\n\n\n\n\n")
for call in categorized_calls:
    print("\n")
    print(call)
    print(call['cdr_record'])
    print(call['cdr_record_aa'])
