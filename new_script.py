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

# result = module_funcs.get_cdr_by_department(start_timestamp, end_timestamp, "main")
# departmentStats_main = classes.DepartmentStats("main")
# module_funcs.count_calls(departmentStats_main, result)
# print(departmentStats_main)
#
# result = module_funcs.get_cdr_by_department(start_timestamp, end_timestamp, "1801")
# departmentStats_1801 = classes.DepartmentStats("1801")
# module_funcs.count_calls(departmentStats_1801, result)
# print(departmentStats_1801)
#
# result = module_funcs.get_cdr_by_department(start_timestamp, end_timestamp, "1200")
# departmentStats_1200 = classes.DepartmentStats("1200")
# module_funcs.count_calls(departmentStats_1200, result)
# print(departmentStats_1200)

result = module_funcs.get_cdr_by_department(start_timestamp, end_timestamp, "ortho")
departmentStats_ortho = classes.DepartmentStats("ortho")
module_funcs.count_calls(departmentStats_ortho, result)
print(departmentStats_ortho)

result = module_funcs.get_cdr_by_department(start_timestamp, end_timestamp, "uro")
departmentStats_uro = classes.DepartmentStats("uro")
module_funcs.count_calls(departmentStats_uro, result)
print(departmentStats_uro)

print("\n\nRutime = ", datetime.datetime.now() - run_start)

# result = module_funcs.get_cdr_record_by_callID("15265399")
# for row in result:
#     print(datetime.datetime.fromtimestamp(int(row[3])))
#     print(row)



