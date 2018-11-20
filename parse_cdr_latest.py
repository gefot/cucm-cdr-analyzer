import os
import time, datetime
import glob
import pytz


CDR_FOLDER = "/home/cdr/cdr_data/"

date = datetime.datetime.now()
today = date.strftime('%Y')+date.strftime('%m')+date.strftime('%d')
# print(today)
# today = "20181119"

files = glob.glob(CDR_FOLDER+"cdr*{}*".format(today))
newest = max(files, key = os.path.getctime)

cst = pytz.timezone('US/Central')
fd = open(CDR_FOLDER+newest, "r")
for line in fd:
    try:
        list = line.split(',')
        date = datetime.datetime.fromtimestamp(int(list[4])).astimezone(cst)
        print(date, list[2], list[8], list[29], list[30], list[49],
              time.strftime("%M:%S", time.gmtime(int(int(list[55])))), list[57])
    except Exception as ex:
        pass

print(newest)