import os
import datetime
from pathlib import Path


####################################################################################################
# CDR filename is in UTC. Timestamps inside CDR files are in client's CUCM timezone.

# Starting from index 1:
# 3:  globalCallID_callId
# 5:  Date (in UTC timezone)
# 9:  calling number
# 30: called number
# 31: final called number
# 50: lastRedirectDn
# 56: duration
# 57: origDeviceName
# 58: destDeviceName

# Business hours
# Main: Mon-Sun 6am-10pm
# Shannon: Mon-Thu 8am-5pm, Fri 8am-12pm
# Lyndsey: Mon-Thu 8am-5pm, Fri 8am-4pm



def is_cdr_date(date, target_unit):
    # print(date)
    hour = int(date.strftime('%H'))
    weekday = date.weekday()

    # Main Hospital Business Hours
    if (target_unit == "main" and (
            weekday == 0 or weekday == 1 or weekday == 2 or weekday == 3 or weekday == 4 or weekday == 5 or weekday == 6) and (
            hour >= 6 and hour <= 21)):
        return True

    # Shannon Clinic Business Hours
    if (target_unit == "shannon" and (
            ((weekday == 0 or weekday == 1 or weekday == 2 or weekday == 3) and (hour >= 8 and hour <= 16)) or (
            (weekday == 4) and (hour >= 8 and hour <= 11)))):
        return True

    # Lyndsey Clinic Business Hours
    if (target_unit == "lyndsey" and (
            ((weekday == 0 or weekday == 1 or weekday == 2 or weekday == 3) and (hour >= 8 and hour <= 16)) or (
            (weekday == 4) and (hour >= 8 and hour <= 15)))):
        return True

    return False


def create_html_file(total_calls, answered_calls, aa_calls, unanswered_calls, total_calls_list, answered_calls_list,
                     aa_calls_list, unanswered_calls_list, answered_calls_per_list, aa_calls_per_list,
                     unanswered_calls_per_list, filename, clinic_names, start, end):
    html_text = """<HTML>
<HEAD>
<STYLE>
td {
    text-align:center;
    padding:4px;
}
</STYLE>
</HEAD>
<BODY>"""

    for key in total_calls_list.keys():
        html_text += "<hr>"
        html_text += "<p>" + clinic_names[key] + "</p>\n"

        html_text += "<TABLE>\n"

        html_text += "<TR>\n"
        html_text += "<TD><b></b></TD>"
        for i in range(start, end):
            html_text += "<TD><b>" + str(i) + "</b></TD>"
        html_text += "<TD><b>Total</b></TD>"
        html_text += "\n</TR>\n"

        html_text += "<TR>"
        html_text += "\n<TD>Calls Answered #</TD>"
        for i in range(start, end):
            html_text += "<TD>" + str(answered_calls_list[key][i]) + "</TD>"
        html_text += "<TD>" + str(answered_calls[key]) + "</TD>"
        html_text += "\n</TR>\n"

        html_text += "<TR>"
        html_text += "\n<TD>Calls Answered %</TD>"
        for i in range(start, end):
            html_text += "<TD>" + str(answered_calls_per_list[key][i]) + "%</TD>"
        if total_calls[key] > 0:
            html_text += "<TD>" + str(round(float(answered_calls[key]) / total_calls[key] * 100, 1)) + "%</TD>"
        else:
            html_text += "<TD>" + "0.0" + "%</TD>"
        html_text += "\n</TR>\n"

        html_text += "<TR>"
        html_text += "\n<TD>Auto Attendant #</TD>"
        for i in range(start, end):
            html_text += "<TD>" + str(aa_calls_list[key][i]) + "</TD>"
        html_text += "<TD>" + str(aa_calls[key]) + "</TD>"
        html_text += "\n</TR>\n"

        html_text += "<TR>"
        html_text += "\n<TD>Auto Attendant %</TD>"
        for i in range(start, end):
            html_text += "<TD>" + str(aa_calls_per_list[key][i]) + "%</TD>"
        if total_calls[key] > 0:
            html_text += "<TD>" + str(round(float(aa_calls[key]) / total_calls[key] * 100, 1)) + "%</TD>"
        else:
            html_text += "<TD>" + "0.0" + "%</TD>"
        html_text += "\n</TR>\n"

        html_text += "<TR>"
        html_text += "\n<TD>Calls Unanswered #</TD>"
        for i in range(start, end):
            html_text += "<TD>" + str(unanswered_calls_list[key][i]) + "</TD>"
        html_text += "<TD>" + str(unanswered_calls[key]) + "</TD>"
        html_text += "\n</TR>\n"

        html_text += "<TR>"
        html_text += "\n<TD>Calls Unanswered %</TD>"
        for i in range(start, end):
            html_text += "<TD>" + str(unanswered_calls_per_list[key][i]) + "%</TD>"
        if total_calls[key] > 0:
            html_text += "<TD>" + str(round(float(unanswered_calls[key]) / total_calls[key] * 100, 1)) + "%</TD>"
        else:
            html_text += "<TD>" + "0.0" + "%</TD>"
        html_text += "\n</TR>\n"

        html_text += "<TR>"
        html_text += "\n<TD><b>Call Volume</b></TD>"
        for i in range(start, end):
            html_text += "<TD><b>" + str(total_calls_list[key][i]) + "</b></TD>"
        html_text += "<TD><b>" + str(total_calls[key]) + "</b></TD>"
        html_text += "\n</TR>\n"

        html_text += "</TABLE>\n"

        html_text += "\n</BODY>\n</HTML>\n"
    html_text += "<hr>"

    fd = open(filename, "w")
    fd.write(html_text)
    fd.close()

    return 0


def create_csv_file(total_calls, answered_calls, aa_calls, unanswered_calls, total_calls_list, answered_calls_list,
                    aa_calls_list, unanswered_calls_list, answered_calls_per_list, aa_calls_per_list,
                    unanswered_calls_per_list, filename, clinic_names, start, end):
    csv_text = ""

    for key in total_calls_list.keys():
        csv_text += "\n" + clinic_names[key]

        csv_text += ","
        for i in range(start, end):
            csv_text += str(i) + ","
        csv_text += "Total\n"

        csv_text += "Calls Answered #,"
        for i in range(start, end):
            csv_text += str(answered_calls_list[key][i]) + ","
        csv_text += str(answered_calls[key]) + "\n"
        csv_text += "Calls Answered %,"
        for i in range(start, end):
            csv_text += str(answered_calls_per_list[key][i]) + ","
        if total_calls[key] > 0:
            csv_text += str(round(float(answered_calls[key]) / total_calls[key] * 100, 1)) + "\n"
        else:
            csv_text += "<TD>" + "0.0" + "%</TD>"

        csv_text += "Auto Attendant #,"
        for i in range(start, end):
            csv_text += str(aa_calls_list[key][i]) + ","
        csv_text += str(aa_calls[key]) + "\n"
        csv_text += "Auto Attendant %,"
        for i in range(start, end):
            csv_text += str(aa_calls_per_list[key][i]) + ","
        if total_calls[key] > 0:
            csv_text += str(round(float(aa_calls[key]) / total_calls[key] * 100, 1)) + "\n"
        else:
            csv_text += "<TD>" + "0.0" + "%</TD>"

        csv_text += "Calls Unanswered #,"
        for i in range(start, end):
            csv_text += str(unanswered_calls_list[key][i]) + ","
        csv_text += str(unanswered_calls[key]) + "\n"
        csv_text += "Calls Unanswered %,"
        for i in range(start, end):
            csv_text += str(unanswered_calls_per_list[key][i]) + ","
        if total_calls[key] > 0:
            csv_text += str(round(float(unanswered_calls[key]) / total_calls[key] * 100, 1)) + "\n"
        else:
            csv_text += "<TD>" + "0.0" + "%</TD>"

        csv_text += "Call Volume,"
        for i in range(start, end):
            csv_text += str(total_calls_list[key][i]) + ","
        csv_text += str(total_calls[key]) + "\n"

    fd = open(filename, "w")
    fd.write(csv_text)
    fd.close()

    return 0


####################################################################################################
# MAIN #
start = datetime.datetime.now()

CDR_FOLDER = '/home/gfot/cdr/cdr_data_daily/'  # Linux
MONTHLY_REPORT_TXT_FILE = '/home/gfot/cucm-cdr-analyzer/data/output/pd_daily_html.txt'
MONTHLY_REPORT_CSV_FILE = '/home/gfot/cucm-cdr-analyzer/data/output/pd_daily_report.csv'
HOURLY_REPORT_TXT_FILE = '/home/gfot/cucm-cdr-analyzer/data/output/pd_hourly_html.txt'
HOURLY_REPORT_CSV_FILE = '/home/gfot/cucm-cdr-analyzer/data/output/pd_hourly_report.csv'

# List directory files only with CDR files
cdr_list = []
for x in os.listdir(CDR_FOLDER):
    if x.startswith("cdr_Stand"):
        cdr_list.append(x)
# print(cdr_list)

# Initialize Variables
# clinic_names = {'main': 'Main Hospital', 'shannon': '1801 Clinic', 'lyndsey': '1200 Clinic'}
clinic_names = {'main': 'Main Hospital', 'shannon': '1801 Clinic'}

# total_calls = {'main': 0, 'shannon': 0, 'lyndsey': 0}
total_calls = {'main': 0, 'shannon': 0}
# answered_calls = {'main': 0, 'shannon': 0, 'lyndsey': 0}
answered_calls = {'main': 0, 'shannon': 0}
# aa_calls = {'main': 0, 'shannon': 0, 'lyndsey': 0}
aa_calls = {'main': 0, 'shannon': 0}
# unanswered_calls = {'main': 0, 'shannon': 0, 'lyndsey': 0}
unanswered_calls = {'main': 0, 'shannon': 0}

# total_calls_list = {'main': [0 for i in range(32)], 'shannon': [0 for i in range(32)], 'lyndsey': [0 for i in range(32)]}
total_calls_list = {'main': [0 for i in range(32)], 'shannon': [0 for i in range(32)]}
# answered_calls_list = {'main': [0 for i in range(32)], 'shannon': [0 for i in range(32)], 'lyndsey': [0 for i in range(32)]}
answered_calls_list = {'main': [0 for i in range(32)], 'shannon': [0 for i in range(32)]}
# aa_calls_list = {'main': [0 for i in range(32)], 'shannon': [0 for i in range(32)], 'lyndsey': [0 for i in range(32)]}
aa_calls_list = {'main': [0 for i in range(32)], 'shannon': [0 for i in range(32)]}
# unanswered_calls_list = {'main': [0 for i in range(32)], 'shannon': [0 for i in range(32)], 'lyndsey': [0 for i in range(32)]}
unanswered_calls_list = {'main': [0 for i in range(32)], 'shannon': [0 for i in range(32)]}

# answered_calls_per_list = {'main': [0 for i in range(32)], 'shannon': [0 for i in range(32)], 'lyndsey': [0 for i in range(32)]}
answered_calls_per_list = {'main': [0 for i in range(32)], 'shannon': [0 for i in range(32)]}
# aa_calls_per_list = {'main': [0 for i in range(32)], 'shannon': [0 for i in range(32)], 'lyndsey': [0 for i in range(32)]}
aa_calls_per_list = {'main': [0 for i in range(32)], 'shannon': [0 for i in range(32)]}
# unanswered_calls_per_list = {'main': [0 for i in range(32)], 'shannon': [0 for i in range(32)], 'lyndsey': [0 for i in range(32)]}
unanswered_calls_per_list = {'main': [0 for i in range(32)], 'shannon': [0 for i in range(32)]}

# total_calls_hourly = {'main': 0, 'shannon': 0, 'lyndsey': 0}
total_calls_hourly = {'main': 0, 'shannon': 0}
# answered_calls_hourly = {'main': 0, 'shannon': 0, 'lyndsey': 0}
answered_calls_hourly = {'main': 0, 'shannon': 0}
# aa_calls_hourly = {'main': 0, 'shannon': 0, 'lyndsey': 0}
aa_calls_hourly = {'main': 0, 'shannon': 0}
# unanswered_calls_hourly = {'main': 0, 'shannon': 0, 'lyndsey': 0}
unanswered_calls_hourly = {'main': 0, 'shannon': 0}

# total_calls_list_hourly = {'main': [0 for i in range(24)], 'shannon': [0 for i in range(24)], 'lyndsey': [0 for i in range(24)]}
total_calls_list_hourly = {'main': [0 for i in range(24)], 'shannon': [0 for i in range(24)]}
# answered_calls_list_hourly = {'main': [0 for i in range(24)], 'shannon': [0 for i in range(24)], 'lyndsey': [0 for i in range(24)]}
answered_calls_list_hourly = {'main': [0 for i in range(24)], 'shannon': [0 for i in range(24)]}
# aa_calls_list_hourly = {'main': [0 for i in range(24)], 'shannon': [0 for i in range(24)], 'lyndsey': [0 for i in range(24)]}
aa_calls_list_hourly = {'main': [0 for i in range(24)], 'shannon': [0 for i in range(24)]}
# unanswered_calls_list_hourly = {'main': [0 for i in range(24)], 'shannon': [0 for i in range(24)], 'lyndsey': [0 for i in range(24)]}
unanswered_calls_list_hourly = {'main': [0 for i in range(24)], 'shannon': [0 for i in range(24)]}

# answered_calls_per_list_hourly = {'main': [0 for i in range(24)], 'shannon': [0 for i in range(24)], 'lyndsey': [0 for i in range(24)]}
answered_calls_per_list_hourly = {'main': [0 for i in range(24)], 'shannon': [0 for i in range(24)]}
# aa_calls_per_list_hourly = {'main': [0 for i in range(24)], 'shannon': [0 for i in range(24)], 'lyndsey': [0 for i in range(24)]}
aa_calls_per_list_hourly = {'main': [0 for i in range(24)], 'shannon': [0 for i in range(24)]}
# unanswered_calls_per_list_hourly = {'main': [0 for i in range(24)], 'shannon': [0 for i in range(24)], 'lyndsey': [0 for i in range(24)]}
unanswered_calls_per_list_hourly = {'main': [0 for i in range(24)], 'shannon': [0 for i in range(24)]}

####################################################################################################
# Calculate CDR Statistics
for file in cdr_list:
    fd = open(CDR_FOLDER + file, "r")
    # print(file)
    for line in fd:
        try:
            list = line.split(',')
            date = datetime.datetime.fromtimestamp(int(list[4]))
            day = int(date.strftime('%d'))
            hour = int(date.strftime('%H'))

            # Main Hospital
            if (len(list[8]) == 12 and "\"1001\"" in list[29]):
                key = 'main'
                if is_cdr_date(date, "main"):
                    # print("\n---\n",list[4], list[29], list[30], list[49], list[55])
                    total_calls[key] += 1
                    total_calls_list[key][day] += 1

                    total_calls_hourly[key] += 1
                    total_calls_list_hourly[key][hour] += 1
                    # Calls answered by operator or 2nd, 3rd line...
                    if (("1001" in list[30] or "5701" in list[30] or "5702" in list[30] or "5703" in list[
                        30] or "5704" in list[30] or "5705" in list[30]) and list[55] is not "0"):
                        answered_calls[key] += 1
                        answered_calls_list[key][day] += 1

                        answered_calls_hourly[key] += 1
                        answered_calls_list_hourly[key][hour] += 1
                    elif ("5500" in list[30] and list[55] is not "0"):
                        aa_calls[key] += 1
                        aa_calls_list[key][day] += 1

                        aa_calls_hourly[key] += 1
                        aa_calls_list_hourly[key][hour] += 1
                    elif (list[55] is "0"):
                        unanswered_calls[key] += 1
                        unanswered_calls_list[key][day] += 1

                        unanswered_calls_hourly[key] += 1
                        unanswered_calls_list_hourly[key][hour] += 1
                    else:
                        answered_calls[key] += 1
                        answered_calls_list[key][day] += 1

                        answered_calls_hourly[key] += 1
                        answered_calls_list_hourly[key][hour] += 1

            # Shannon Clinic
            elif (len(list[8]) == 12 and "\"5810\"" in list[29]):
                key = 'shannon'
                if is_cdr_date(date, "shannon"):
                    total_calls[key] += 1
                    total_calls_list[key][day] += 1

                    total_calls_hourly[key] += 1
                    total_calls_list_hourly[key][hour] += 1
                    if ("5810" in list[30] and list[55] is not "0"):
                        answered_calls[key] += 1
                        answered_calls_list[key][day] += 1

                        answered_calls_hourly[key] += 1
                        answered_calls_list_hourly[key][hour] += 1
                    elif ("5500" in list[30] and list[55] is not "0"):
                        aa_calls[key] += 1
                        aa_calls_list[key][day] += 1

                        aa_calls_hourly[key] += 1
                        aa_calls_list_hourly[key][hour] += 1
                    elif (list[55] is "0"):
                        unanswered_calls[key] += 1
                        unanswered_calls_list[key][day] += 1

                        unanswered_calls_hourly[key] += 1
                        unanswered_calls_list_hourly[key][hour] += 1
                    else:
                        answered_calls[key] += 1
                        answered_calls_list[key][day] += 1

                        answered_calls_hourly[key] += 1
                        answered_calls_list_hourly[key][hour] += 1
            ################
            # Lyndsey Clinic
            if (len(list[8]) >= 12 and (
                    "\"5850\"" in list[29] or "8307742505" in list[29] or "8307757555" in list[29] or "8303137138" in
                    list[29])):
                key = 'lyndsey'
                if (is_cdr_date(date, "lyndsey")):
                    total_calls[key] += 1
                    total_calls_list[key][day] += 1

                    total_calls_hourly[key] += 1
                    total_calls_list_hourly[key][hour] += 1
                    if (("5850" in list[30] or "8307742505" in list[30] or "8307757555" in list[30] or "8303137138" in
                         list[30]) and list[55] is not "0"):
                        answered_calls[key] += 1
                        answered_calls_list[key][day] += 1

                        answered_calls_hourly[key] += 1
                        answered_calls_list_hourly[key][hour] += 1
                    elif ("5500" in list[30] and list[55] is not "0"):
                        aa_calls[key] += 1
                        aa_calls_list[key][day] += 1

                        aa_calls_hourly[key] += 1
                        aa_calls_list_hourly[key][hour] += 1
                    elif (list[55] is "0"):
                        unanswered_calls[key] += 1
                        unanswered_calls_list[key][day] += 1

                        unanswered_calls_hourly[key] += 1
                        unanswered_calls_list_hourly[key][hour] += 1
                    else:
                        answered_calls[key] += 1
                        answered_calls_list[key][day] += 1

                        answered_calls_hourly[key] += 1
                        answered_calls_list_hourly[key][hour] += 1

        except:
            # print("General Exception")
            continue

####################################################################################################
# Calculate Percentages
for key in total_calls.keys():
    for i in range(1, 32):
        if (answered_calls_list[key][i]) > 0:
            answered_calls_per_list[key][i] = round(float(answered_calls_list[key][i]) / total_calls_list[key][i] * 100,
                                                    1)
        else:
            answered_calls_per_list[key][i] = 0.0
        if (aa_calls_list[key][i]) > 0:
            aa_calls_per_list[key][i] = round(float(aa_calls_list[key][i]) / total_calls_list[key][i] * 100, 1)
        else:
            aa_calls_per_list[key][i] = 0.0
        if (unanswered_calls_list[key][i]) > 0:
            unanswered_calls_per_list[key][i] = round(
                float(unanswered_calls_list[key][i]) / total_calls_list[key][i] * 100, 1)
        else:
            unanswered_calls_per_list[key][i] = 0.0

for key in total_calls.keys():
    for i in range(0, 23):
        if (answered_calls_list_hourly[key][i]) > 0:
            answered_calls_per_list_hourly[key][i] = round(
                float(answered_calls_list_hourly[key][i]) / total_calls_list_hourly[key][i] * 100, 1)
        else:
            answered_calls_per_list_hourly[key][i] = 0.0
        if (aa_calls_list_hourly[key][i]) > 0:
            aa_calls_per_list_hourly[key][i] = round(
                float(aa_calls_list_hourly[key][i]) / total_calls_list_hourly[key][i] * 100, 1)
        else:
            aa_calls_per_list_hourly[key][i] = 0.0
        if (unanswered_calls_list_hourly[key][i]) > 0:
            unanswered_calls_per_list_hourly[key][i] = round(
                float(unanswered_calls_list_hourly[key][i]) / total_calls_list_hourly[key][i] * 100, 1)
        else:
            unanswered_calls_per_list_hourly[key][i] = 0.0

####################################################################################################
# Print CDR Statistics
print("\n=======================================")
for key in total_calls.keys():
    print("\nTotal Results for", key)
    print("total_calls =", total_calls[key])
    print("answered_calls =", answered_calls[key])
    print("aa_calls =", aa_calls[key])
    print("unanswered_calls =", unanswered_calls[key])

for key in total_calls_list.keys():
    print("\nResults list for", key)
    print("total_calls_list =", total_calls_list[key])
    print("answered_calls_list =", answered_calls_list[key])
    print("aa_calls_list =", aa_calls_list[key])
    print("unanswered_calls_list =", unanswered_calls_list[key])

for key in total_calls.keys():
    print("\nTotal Results_hourly for", key)
    print("total_calls_hourly =", total_calls_hourly[key])
    print("answered_calls_hourly =", answered_calls_hourly[key])
    print("aa_calls_hourly =", aa_calls_hourly[key])
    print("unanswered_calls_hourly =", unanswered_calls_hourly[key])

for key in total_calls_list.keys():
    print("\nResults list for", key)
    print("total_calls_list_hourly =", total_calls_list_hourly[key])
    print("answered_calls_list_hourly =", answered_calls_list_hourly[key])
    print("aa_calls_list_hourly =", aa_calls_list_hourly[key])
    print("unanswered_calls_list_hourly =", unanswered_calls_list_hourly[key])

# Print CDR Percentages
print("\n")
for key in total_calls_list.keys():
    print("\nPercentage results list for", key)
    print("answered_calls_per_list =", answered_calls_per_list[key])
    print("aa_calls_per_list =", aa_calls_per_list[key])
    print("unanswered_calls_per_list =", unanswered_calls_per_list[key])

print("\n")
for key in total_calls_list_hourly.keys():
    print("\nPercentage results list for", key)
    print("answered_calls_per_list_hourly =", answered_calls_per_list_hourly[key])
    print("aa_calls_per_list_hourly =", aa_calls_per_list_hourly[key])
    print("unanswered_calls_per_list_hourly =", unanswered_calls_per_list_hourly[key])

####################################################################################################
# Create files
create_html_file(total_calls, answered_calls, aa_calls, unanswered_calls, total_calls_list, answered_calls_list,
                 aa_calls_list, unanswered_calls_list, answered_calls_per_list, aa_calls_per_list,
                 unanswered_calls_per_list, MONTHLY_REPORT_TXT_FILE, clinic_names, 1, 32)
create_csv_file(total_calls, answered_calls, aa_calls, unanswered_calls, total_calls_list, answered_calls_list,
                aa_calls_list, unanswered_calls_list, answered_calls_per_list, aa_calls_per_list,
                unanswered_calls_per_list, MONTHLY_REPORT_CSV_FILE, clinic_names, 1, 32)

create_html_file(total_calls_hourly, answered_calls_hourly, aa_calls_hourly, unanswered_calls_hourly,
                 total_calls_list_hourly, answered_calls_list_hourly, aa_calls_list_hourly,
                 unanswered_calls_list_hourly, answered_calls_per_list_hourly, aa_calls_per_list_hourly,
                 unanswered_calls_per_list_hourly, HOURLY_REPORT_TXT_FILE, clinic_names, 0, 24)
create_csv_file(total_calls_hourly, answered_calls_hourly, aa_calls_hourly, unanswered_calls_hourly,
                total_calls_list_hourly, answered_calls_list_hourly, aa_calls_list_hourly, unanswered_calls_list_hourly,
                answered_calls_per_list_hourly, aa_calls_per_list_hourly, unanswered_calls_per_list_hourly,
                HOURLY_REPORT_CSV_FILE, clinic_names, 0, 24)

# Measure Script Execution
print("\n\nRutime = ", datetime.datetime.now() - start)

####################################################################################################
