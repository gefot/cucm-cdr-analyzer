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

result = module_funcs.get_cdr_by_department(start_timestamp, end_timestamp, "main")
main_departmentStats = classes.DepartmentStats("main")
module_funcs.count_calls(main_departmentStats, result)
print(main_departmentStats)

print("\n\nRutime = ", datetime.datetime.now() - run_start)

# for row in result:
#     print(datetime.datetime.fromtimestamp(int(row[3])))
#     print(row)



# module_funcs.populate_db()
