import datetime

from modules import module_funcs
from modules import classes

run_start = datetime.datetime.now()

start_date = "20190916060000"
end_date   = "20190920235900"
start_timestamp = module_funcs.date_to_timestamp(start_date)
end_timestamp = module_funcs.date_to_timestamp(end_date)

# result = module_funcs.get_cdr(start_timestamp, end_timestamp, "*", "*")

print("\n\n\n----->Main Hospital")
cdr_records = module_funcs.get_cdr_by_called_number(start_timestamp, end_timestamp, "1001")
departmentStats_main = classes.callTreeStats("main")
module_funcs.count_calls_by_call_tree(departmentStats_main, cdr_records)
print(departmentStats_main)

print("\n\n\n----->1801 Clinic")
cdr_records = module_funcs.get_cdr_by_called_number(start_timestamp, end_timestamp, "5810")
departmentStats_1801 = classes.callTreeStats("1801")
module_funcs.count_calls_by_call_tree(departmentStats_1801, cdr_records)
print(departmentStats_1801)

print("\n\n\n----->1200 Clinic")
cdr_records = module_funcs.get_cdr_by_called_number(start_timestamp, end_timestamp, "5850")
departmentStats_1200 = classes.callTreeStats("1200")
module_funcs.count_calls_by_call_tree(departmentStats_1200, cdr_records)
print(departmentStats_1200)

print("\n\n\n----->Ortho Clinic")
cdr_records = module_funcs.get_cdr_by_called_number(start_timestamp, end_timestamp, "7002")
extensionStats_ortho = classes.ExtensionStats("7002")
module_funcs.count_calls_by_extension(extensionStats_ortho, cdr_records)
print(extensionStats_ortho)

print("\n\n\n----->Uro Clinic")
cdr_records = module_funcs.get_cdr_by_called_number(start_timestamp, end_timestamp, "1733")
extensionStats_uro = classes.ExtensionStats("1733")
module_funcs.count_calls_by_extension(extensionStats_uro, cdr_records)
print(extensionStats_uro)

print("\n\n\n----->IT Helpdesk")
cdr_records = module_funcs.get_cdr_by_called_number(start_timestamp, end_timestamp, "3333")
huntpilotStats_it = classes.HuntPilotStats("3333")
module_funcs.count_calls_by_hunt_pilot(huntpilotStats_it, cdr_records)
print(huntpilotStats_it)


print("\n\nRutime = ", datetime.datetime.now() - run_start)

cdr_records = module_funcs.get_cdr_record_by_callID("15230047")
for cdr_record in cdr_records:
    print(datetime.datetime.fromtimestamp(int(cdr_record[3])))
    print(cdr_record)



