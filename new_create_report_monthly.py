import datetime
import module_funcs


start = datetime.datetime.now()
today = datetime.date.today()
my_month = today.strftime('%b')
my_year = today.strftime('%Y')

my_type1 = "daily"
my_type2 = "hourly"

call_tree1 = "main"
filename1_1 = "/home/gfot/cucm-cdr-analyzer/data/output/" + call_tree1 + "_daily_" + my_month + "_" + my_year + ".csv"
filename1_2 = "/home/gfot/cucm-cdr-analyzer/data/output/" + call_tree1 + "_hourly_" + my_month + "_" + my_year + ".csv"

call_tree2 = "1801"
filename2_1 = "/home/gfot/cucm-cdr-analyzer/data/output/" + call_tree1 + "_daily_" + my_month + "_" + my_year + ".csv"
filename2_2 = "/home/gfot/cucm-cdr-analyzer/data/output/" + call_tree1 + "_hourly_" + my_month + "_" + my_year + ".csv"

STARTDATE = "201909100001"
ENDDATE = "201909102359"

cdr_file_list = module_funcs.get_cdr_files(STARTDATE, ENDDATE)
[print(cdr_file) for cdr_file in cdr_file_list]

categorized_calls1 = module_funcs.categorize_cdr_general(cdr_file_list, call_tree1)
# counted_calls_daily1, counted_calls_hourly1 = module_funcs.count_categorized_calls(categorized_calls1)
# module_funcs.create_reports_csv(filename1_1, my_type1, counted_calls_daily1)
# module_funcs.create_reports_csv(filename1_2, my_type2, counted_calls_hourly1)
#
# categorized_calls2 = module_funcs.categorize_cdr_general(cdr_file_list, call_tree2)
# counted_calls_daily2, counted_calls_hourly2 = module_funcs.count_categorized_calls(categorized_calls2)
# module_funcs.create_reports_csv(filename2_1, my_type1, counted_calls_daily2)
# module_funcs.create_reports_csv(filename2_2, my_type2, counted_calls_hourly2)


print("\n--->Runtime = {} \n\n\n".format(datetime.datetime.now() - start))
