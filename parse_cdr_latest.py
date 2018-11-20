import os
import datetime
import glob


date = datetime.datetime.now()
today = date.strftime('%Y')+date.strftime('%m')+date.strftime('%d')
print(today)
today = "20181119"

#filename =
files = glob.glob("/home/cdr/cdr_data/cdr*{}*".format(today))
newest = max(files, key = os.path.getctime)
print(newest)