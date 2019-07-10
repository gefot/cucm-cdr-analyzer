
import module_funcs

STARTDATE = "201907090000"
ENDDATE = "201907110000"
FILTERS = {'extensions': ["911"]}

cdr_file_list = module_funcs.get_cdr_files(STARTDATE, ENDDATE)
cdr_records = module_funcs.get_cdr_records(cdr_file_list, FILTERS)

for cdr_record in cdr_records:
    print(cdr_record)
