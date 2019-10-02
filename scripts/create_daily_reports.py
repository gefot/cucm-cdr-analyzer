import datetime

from modules import module_funcs
from modules import classes


date = "20190911000000"
# date = datetime.datetime.today().strftime('%Y%m%d%H%M%S')

# start_date = "20190916060000"
# end_date   = "20190920235900"
# start_timestamp = module_funcs.date_to_timestamp(start_date)
# end_timestamp = module_funcs.date_to_timestamp(end_date)

day_timestamp_range = module_funcs.day_timestamp_range_from_date(date)
start_timestamp = day_timestamp_range[0]
end_timestamp   = day_timestamp_range[1]

print("\n\n\n----->Main Hospital")
cdr_records = module_funcs.get_cdr_by_called_number(start_timestamp, end_timestamp, "1001")
departmentStats_main = classes.DepartmentStats("main")
module_funcs.count_calls_by_call_tree(departmentStats_main, cdr_records)
departmentStats_main.populate_percentages()
print(departmentStats_main)

print("\n\n\n----->1801 Clinic")
cdr_records = module_funcs.get_cdr_by_called_number(start_timestamp, end_timestamp, "5810")
departmentStats_1801 = classes.DepartmentStats("1801")
module_funcs.count_calls_by_call_tree(departmentStats_1801, cdr_records)
departmentStats_1801.populate_percentages()
print(departmentStats_1801)

print("\n\n\n----->1200 Clinic")
cdr_records = module_funcs.get_cdr_by_called_number(start_timestamp, end_timestamp, "5850")
departmentStats_1200 = classes.DepartmentStats("1200")
module_funcs.count_calls_by_call_tree(departmentStats_1200, cdr_records)
departmentStats_1200.populate_percentages()
print(departmentStats_1200)

print("\n\n\n----->Ortho Clinic")
cdr_records = module_funcs.get_cdr_by_called_number(start_timestamp, end_timestamp, "7002")
extensionStats_ortho = classes.ExtensionStats("7002")
module_funcs.count_calls_by_extension(extensionStats_ortho, cdr_records)
extensionStats_ortho.populate_percentages()
print(extensionStats_ortho)

print("\n\n\n----->Uro Clinic")
cdr_records = module_funcs.get_cdr_by_called_number(start_timestamp, end_timestamp, "1733")
extensionStats_uro = classes.ExtensionStats("1733")
module_funcs.count_calls_by_extension(extensionStats_uro, cdr_records)
extensionStats_uro.populate_percentages()
print(extensionStats_uro)

print("\n\n\n----->IT Helpdesk")
cdr_records = module_funcs.get_cdr_by_called_number(start_timestamp, end_timestamp, "3333")
huntpilotStats_it = classes.HuntPilotStats("3333")
module_funcs.count_calls_by_hunt_pilot(huntpilotStats_it, cdr_records)
huntpilotStats_it.populate_percentages()
print(huntpilotStats_it)

