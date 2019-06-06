import module_funcs

STARTDATE = "201905080100"
ENDDATE = "201905082300"
CALL_TREE = "main"

cdr_file_list = module_funcs.get_cdr_files(STARTDATE, ENDDATE)
categorized_calls = module_funcs.categorize_cdr_general(cdr_file_list, CALL_TREE)

answered_1st = 0
unanswered_1st = 0
total_aa = 0

# module_funcs.create_daily_report(STARTDATE, ENDDATE, categorized_calls)

for call in categorized_calls:
    if call.type == "aa":
        pass
        # print("\n")
        # print(call.cdr_record)
        # print(call.cdr_record_aa)
        # print(call)

    if call.type == "1st level" and call.handle == 'answered':
        answered_1st += 1
    if call.type == "1st level" and call.handle == 'unanswered':
        unanswered_1st += 1
    if call.type == "aa":
        total_aa += 1

print(answered_1st)
print(total_aa)
print(unanswered_1st)
