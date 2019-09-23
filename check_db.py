import module_funcs

import datetime
import time

timestamp = 1567614099
dt_object = datetime.datetime.fromtimestamp(timestamp)
print("dt_object =", dt_object)

my_date = datetime.datetime.now()
my_date = "20190922163012"
# my_date = "20190922"

timestamp = time.mktime(datetime.datetime.strptime(my_date, "%Y%m%d%H%M%S").timetuple())
# timestamp = datetime.datetime.timestamp(my_date)
print("timestamp =", timestamp)

dt_object = datetime.datetime.fromtimestamp(timestamp)
print("dt_object =", dt_object)

# module_funcs.populate_db()

