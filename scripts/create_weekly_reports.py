import datetime

from modules import module_funcs
from modules import classes


# date = "20190911000000"
date = datetime.datetime.today().strftime('%Y%m%d%H%M%S')

# start_date = "20190916060000"
# end_date   = "20190920235900"
# start_timestamp = module_funcs.date_to_timestamp(start_date)
# end_timestamp = module_funcs.date_to_timestamp(end_date)

week_timestamp_range = module_funcs.week_timestamp_range_from_date(date)
start_timestamp = week_timestamp_range[0]
end_timestamp   = week_timestamp_range[1]

print("\n\n\n----->Main Hospital")
cdr_records = module_funcs.get_cdr_by_called_number(start_timestamp, end_timestamp, "1001")
departmentStats_main = classes.DepartmentStats("main")
module_funcs.count_calls_by_call_tree(departmentStats_main, cdr_records)
print(departmentStats_main)

for cdr_record in cdr_records:
    print(datetime.datetime.fromtimestamp(int(cdr_record[3])))
    print(cdr_record)
