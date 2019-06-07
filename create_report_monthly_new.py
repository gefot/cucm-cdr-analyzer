
import datetime
import module_funcs

STARTDATE = "201905010001"
ENDDATE = "201905082359"
CALL_TREE = "shannon"

start = datetime.datetime.now()
today = datetime.date.today()

cdr_file_list = module_funcs.get_cdr_files(STARTDATE, ENDDATE)
print("\n--->Runtime = {} \n\n\n".format(datetime.datetime.now() - start))

categorized_calls = module_funcs.categorize_cdr_general(cdr_file_list, CALL_TREE)
print("\n--->Runtime = {} \n\n\n".format(datetime.datetime.now() - start))

counted_calls_daily, counted_calls_hourly = module_funcs.generate_reports(STARTDATE, ENDDATE, categorized_calls)
print(counted_calls_daily)
print(counted_calls_hourly)
print("\n--->Runtime = {} \n\n\n".format(datetime.datetime.now() - start))

filename = "/home/gfot/cucm-cdr-analyzer/date/monthly_" + today.strftime('%b_%Y') + ".csv"
print(filename)
module_funcs.create_reports_csv(filename, "daily", counted_calls_daily)
print("\n--->Runtime = {} \n\n\n".format(datetime.datetime.now() - start))
