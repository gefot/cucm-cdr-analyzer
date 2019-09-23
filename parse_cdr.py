
import module_funcs

# STARTDATE = "201909200000"
# ENDDATE = "201909202359"
STARTDATE = "201908200000"
ENDDATE   = "201908212359"
FILTERS = {'extensions': ["911"]}
FILTERS = {'extensions': ["*"]}

cdr_file_list = module_funcs.get_cdr_files(STARTDATE, ENDDATE)
print(cdr_file_list)
cdr_records = module_funcs.get_cdr_records(cdr_file_list, FILTERS)

for cdr_record in cdr_records:
    print(cdr_record)
