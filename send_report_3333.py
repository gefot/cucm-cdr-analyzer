import json
from pathlib import Path

import _module_funcs

####################################################################################################
#  MAIN

# access = json.load(open('data/access.json'))                            # Windows
# body_file = 'data/report-3333.txt'                                      # Windows
# DATA_FOLDER = str(Path(__file__).parent) + '\\data\\'                   # Windows

access = json.load(open('/home/pbx/cucm-cdr-analyzer/data/access.json'))  # Linux
body_file = '/home/pbx/cucm-cdr-analyzer/data/report-3333.txt'            # Linux
DATA_FOLDER = '/home/pbx/cucm-cdr-analyzer/data/'                         # Linux


attachments = [DATA_FOLDER + fn for fn in \
                     ['cdr-3333-total.txt', 'cdr-3333-voicemail.txt', 'cdr-3333-unanswered.txt', \
                      'cdr-calls-3691.txt', 'cdr-calls-3334.txt', 'cdr-calls-3730.txt', \
                      'cdr-calls-2547.txt', 'cdr-calls-3686.txt']]

subject = "Weekly Report for x3333 (Mon - Thu: 9am - 5pm)"
fd1 = open(body_file,'r')
body = fd1.read()
fd1.close()

# Send e-mail
USERNAME = str(access["gmail"]["username"])
PASSWORD = str(access["gmail"]["password"])

# toaddr = ['georgios.fotiadis@gmail.com']
toaddr = ['val.king@whitehatvirtual.com', 'georgios.fotiadis@whitehatvirtual.com']
_module_funcs.send_mail(USERNAME, PASSWORD, toaddr, subject, body, attachments)
