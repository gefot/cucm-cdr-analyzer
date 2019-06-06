import module_funcs

STARTDATE = "201905080100"
ENDDATE = "201905082300"
CALL_TREE = "shannon"

cdr_file_list = module_funcs.get_cdr_files(STARTDATE, ENDDATE)

categorized_calls = module_funcs.categorize_cdr_general(cdr_file_list, CALL_TREE)

module_funcs.create_daily_report(STARTDATE, ENDDATE, categorized_calls)

answered_1st = 0
unanswered_1st = 0
total_aa = 0
for call in categorized_calls:
    if call.type == "1st level" and call.handle == 'answered':
        answered_1st += 1
    if call.type == "1st level" and call.handle == 'unanswered':
        unanswered_1st += 1
    if call.type == "aa":
        total_aa += 1
print("\n\n\n")
print(answered_1st)
print(total_aa)
print(unanswered_1st)
