import datetime

import module_funcs
import classes

run_start = datetime.datetime.now()

start_date = "20190916060000"
end_date   = "20190920235900"
# start_date = "20190920060000"
# end_date   = "20190922230000"
start_timestamp = module_funcs.date_to_timestamp(start_date)
end_timestamp = module_funcs.date_to_timestamp(end_date)

# result = module_funcs.get_cdr(start_timestamp, end_timestamp, "*", "*")

# print("\n\n\n----->Main Hospital")
# result = module_funcs.get_cdr_by_called_number(start_timestamp, end_timestamp, "1001")
# departmentStats_main = classes.DepartmentStats("main")
# module_funcs.count_calls_by_call_tree(departmentStats_main, result)
# print(departmentStats_main)
#
# print("\n\n\n----->1801 Clinic")
# result = module_funcs.get_cdr_by_called_number(start_timestamp, end_timestamp, "5810")
# departmentStats_1801 = classes.DepartmentStats("1801")
# module_funcs.count_calls_by_call_tree(departmentStats_1801, result)
# print(departmentStats_1801)
#
# print("\n\n\n----->1200 Clinic")
# result = module_funcs.get_cdr_by_called_number(start_timestamp, end_timestamp, "5850")
# departmentStats_1200 = classes.DepartmentStats("1200")
# module_funcs.count_calls_by_call_tree(departmentStats_1200, result)
# print(departmentStats_1200)

# print("\n\n\n----->Ortho Clinic")
# result = module_funcs.get_cdr_by_called_number(start_timestamp, end_timestamp, "7002")
# extensionStats_ortho = classes.ExtensionStats("7002")
# module_funcs.count_calls_by_extension(extensionStats_ortho, result)
# print(extensionStats_ortho)
#
# print("\n\n\n----->Uro Clinic")
# result = module_funcs.get_cdr_by_called_number(start_timestamp, end_timestamp, "1733")
# extensionStats_uro = classes.ExtensionStats("1733")
# module_funcs.count_calls_by_extension(extensionStats_uro, result)
# print(extensionStats_uro)

result = module_funcs.get_cdr_by_called_number(start_timestamp, end_timestamp, "3333")
huntpilotStats_it = classes.HuntPilotStats("3333")
module_funcs.count_calls_by_hunt_pilot(huntpilotStats_it, result)
print(huntpilotStats_it)


print("\n\nRutime = ", datetime.datetime.now() - run_start)

result = module_funcs.get_cdr_record_by_callID("15261548")
for row in result:
    print(datetime.datetime.fromtimestamp(int(row[3])))
    print(row)



