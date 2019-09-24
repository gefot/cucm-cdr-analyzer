import datetime

import module_funcs

run_start = datetime.datetime.now()

timestamp = 1567614099
date = module_funcs.timestamp_to_date(timestamp)
print(date)

# date = datetime.datetime.now()
date = "20190922163012"
timestamp = module_funcs.date_to_timestamp(date)
print(timestamp)
print(module_funcs.timestamp_to_date(timestamp))

start_date = "20190920060000"
end_date   = "20190922230000"
start_timestamp = module_funcs.date_to_timestamp(start_date)
end_timestamp = module_funcs.date_to_timestamp(end_date)

print(module_funcs.weekday_from_timestamp(start_timestamp))
print(module_funcs.hour_from_timestamp(start_timestamp))

# result = module_funcs.get_cdr(start_timestamp, end_timestamp, "*", "*")
result = module_funcs.get_cdr_by_department(start_timestamp, end_timestamp, "specialty")

print("\n\nRutime = ", datetime.datetime.now() - run_start)

for row in result:
    print(datetime.datetime.fromtimestamp(int(row[3])))
    print(row)



# module_funcs.populate_db()
