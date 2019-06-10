import datetime
import module_funcs

STARTDATE = "201906030001"
ENDDATE = "201906072359"
CALL_TREE = "shannon"

start = datetime.datetime.now()
today = datetime.date.today()
my_month = today.strftime('%b')
my_year = today.strftime('%Y')

cdr_file_list = module_funcs.get_cdr_files(STARTDATE, ENDDATE)
categorized_calls = module_funcs.categorize_cdr_general(cdr_file_list, CALL_TREE)
counted_calls_daily, counted_calls_hourly = module_funcs.count_categorized_calls(categorized_calls)
filename = "/home/gfot/cucm-cdr-analyzer/data/output/daily_" + my_month + "_" + my_year + ".csv"
module_funcs.create_reports_csv(filename, "daily", counted_calls_daily)
filename = "/home/gfot/cucm-cdr-analyzer/data/output/hourly_" + my_month + "_" + my_year + ".csv"
module_funcs.create_reports_csv(filename, "hourly", counted_calls_hourly)


print("\n--->Runtime = {} \n\n\n".format(datetime.datetime.now() - start))
