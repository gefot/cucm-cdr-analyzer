import datetime

from modules import module_funcs
from modules import classes

date = "20190911000000"
OUTPUT_PATH = '/home/gfot/cucm-cdr-analyzer/data/output/'
DEPARTMENTS = {'main': '1001', '1801': '5810', '1200': '5850'}
EXTENSIONS = {'ortho': '7002', 'uro': '1733'}

# date = datetime.datetime.today().strftime('%Y%m%d%H%M%S')

# start_date = "20190916060000"
# end_date   = "20190920235900"
# start_timestamp = module_funcs.date_to_timestamp(start_date)
# end_timestamp = module_funcs.date_to_timestamp(end_date)

day_timestamp_range = module_funcs.day_timestamp_range_from_date(date)
start_timestamp = day_timestamp_range[0]
end_timestamp = day_timestamp_range[1]

# CALL TREES
for department, called_number in DEPARTMENTS.items():
    print("\n\n\n----->{}".format(department))
    cdr_records = module_funcs.get_cdr_by_called_number(start_timestamp, end_timestamp, called_number)
    departmentStats = classes.DepartmentStats(department)
    module_funcs.count_calls_by_call_tree(departmentStats, cdr_records)
    departmentStats.populate_percentages()

    full_filename = OUTPUT_PATH + department + "_daily_" + datetime.datetime.strptime(date, '%Y%m%d%H%M%S').strftime('%Y_%m_%d') + ".csv"
    departmentStats.create_csv_file(full_filename)
    print(full_filename)
    print(departmentStats)

# EXTENSIONS
for department, extension in EXTENSIONS.items():
    print("\n\n\n----->{}".format(department))
    cdr_records = module_funcs.get_cdr_by_called_number(start_timestamp, end_timestamp, extension)
    extensionStats = classes.ExtensionStats(extension)
    module_funcs.count_calls_by_extension(extensionStats, cdr_records)
    extensionStats.populate_percentages()
    print(extensionStats)

# print("\n\n\n----->Ortho Clinic")
# cdr_records = module_funcs.get_cdr_by_called_number(start_timestamp, end_timestamp, "7002")
# extensionStats_ortho = classes.ExtensionStats("7002")
# module_funcs.count_calls_by_extension(extensionStats_ortho, cdr_records)
# extensionStats_ortho.populate_percentages()
# print(extensionStats_ortho)
#
# print("\n\n\n----->Uro Clinic")
# cdr_records = module_funcs.get_cdr_by_called_number(start_timestamp, end_timestamp, "1733")
# extensionStats_uro = classes.ExtensionStats("1733")
# module_funcs.count_calls_by_extension(extensionStats_uro, cdr_records)
# extensionStats_uro.populate_percentages()
# print(extensionStats_uro)
#
# print("\n\n\n----->IT Helpdesk")
# cdr_records = module_funcs.get_cdr_by_called_number(start_timestamp, end_timestamp, "3333")
# huntpilotStats_it = classes.HuntPilotStats("3333")
# module_funcs.count_calls_by_hunt_pilot(huntpilotStats_it, cdr_records)
# huntpilotStats_it.populate_percentages()
# print(huntpilotStats_it)
