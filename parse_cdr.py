
import module_funcs

STARTDATE = "201906040000"
ENDDATE = "201906050000"
FILTERS = {'extensions': ["4208"]}

cdr_file_list = module_funcs.get_cdr_files(STARTDATE, ENDDATE)
cdr_records = module_funcs.get_cdr_records(cdr_file_list, FILTERS)

for cdr_record in cdr_records:
    print(cdr_record)
