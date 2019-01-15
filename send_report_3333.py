
import json

import module_funcs

####################################################################################################
#  MAIN

access = json.load(open('/home/pbx/cucm-cdr-analyzer/data/access.json'))  # Linux
body_file = '/home/pbx/cucm-cdr-analyzer/data/output/report-3333.txt'
OUTPUT_FOLDER = '/home/pbx/cucm-cdr-analyzer/data/output/'

attachments = [OUTPUT_FOLDER + fn for fn in \
                     ['cdr-3333-total.txt', 'cdr-3333-voicemail.txt', 'cdr-3333-unanswered.txt', \
                      'cdr-calls-3691.txt', 'cdr-calls-3334.txt', 'cdr-calls-3730.txt', \
                      'cdr-calls-2547.txt', 'cdr-calls-3686.txt']]

subject = "Weekly Report for x3333 (Mon - Thu: 9am - 5pm)"
fd1 = open(body_file, 'r')
body = fd1.read()
fd1.close()

# Send e-mail
USERNAME = str(access["o365"]["username"])
PASSWORD = str(access["o365"]["password"])
MAIL_SERVER = str(access["o365"]["mail_server"])

# toaddr = ['georgios.fotiadis@gmail.com']
toaddr = ['val.king@whitehatvirtual.com', 'georgios.fotiadis@whitehatvirtual.com']
module_funcs.send_mail(USERNAME, PASSWORD, MAIL_SERVER, toaddr, subject, body, attachments, False, False)
