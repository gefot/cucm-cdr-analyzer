
class DepartmentStats:
    def __init__(self, department):
        self.department = department

        self.total = 0
        self.total_perDay = [0 for i in range(32)]
        self.total_perHour = [0 for i in range(24)]

        self.answered_1stLevel = 0
        self.answered_1stLevel_percent = 0
        self.answered_1stLevel_perDay = [0 for i in range(32)]
        self.answered_1stLevel_perDay_percent = [0 for i in range(32)]
        self.answered_1stLevel_perHour = [0 for i in range(24)]
        self.answered_1stLevel_perHour_percent = [0 for i in range(24)]

        self.missed_1stLevel = 0
        self.missed_1stLevel_percent = 0
        self.missed_1stLevel_perDay = [0 for i in range(32)]
        self.missed_1stLevel_perDay_percent = [0 for i in range(32)]
        self.missed_1stLevel_perHour = [0 for i in range(24)]
        self.missed_1stLevel_perHour_percent = [0 for i in range(24)]

        self.answered_aa = 0
        self.answered_aa_percent = 0
        self.answered_aa_perDay = [0 for i in range(32)]
        self.answered_aa_perDay_percent = [0 for i in range(32)]
        self.answered_aa_perHour = [0 for i in range(24)]
        self.answered_aa_perHour_percent = [0 for i in range(24)]


        # TODO
        self.missed_aa = 0
        self.missed_aa_perDay = [0 for i in range(32)]
        self.missed_aa_perHour = [0 for i in range(24)]

    def __str__(self):
        return "\ntotal: {}\ntotal_perDay: {}\ntotal_perHour: {}" \
               "\n\nanswered_1stLevel: {}" \
               "\nanswered_1stLevel_perDay: {}\nanswered_1stLevel_perDay_percent: {}" \
               "\nanswered_1stLevel_perHour: {}\nanswered_1stLevel_perHour_percent: {}" \
               "\n\nmissed_1stLevel: {}" \
               "\nmissed_1stLevel_perDay: {}\nmissed_1stLevel_perDay_percent: {}" \
               "\nmissed_1stLevel_perHour: {}\nmissed_1stLevel_perHour_percent: {}" \
               "\n\nanswered_aa: {}" \
               "\nanswered_aa_perDay: {}\nanswered_aa_perDay_percent: {}" \
               "\nanswered_aa_perHour: {}\nanswered_aa_perHour_percent: {}".format(
            self.total, self.total_perDay, self.total_perHour,
            self.answered_1stLevel,
            self.answered_1stLevel_perDay, self.answered_1stLevel_perDay_percent,
            self.answered_1stLevel_perHour, self.answered_1stLevel_perHour_percent,
            self.missed_1stLevel,
            self.missed_1stLevel_perDay, self.missed_1stLevel_perDay_percent,
            self.missed_1stLevel_perHour, self.missed_1stLevel_perHour_percent,
            self.answered_aa,
            self.answered_aa_perDay, self.answered_aa_perDay_percent,
            self.answered_aa_perHour, self.answered_aa_perHour_percent)

    def populate_percentages(self):

        for i in range(32):
            try:
                self.answered_1stLevel_perDay_percent[i] = str(round(float(self.answered_1stLevel_perDay[i]) / self.total_perDay[i] * 100, 1)) + "%"
            except:
                self.answered_1stLevel_perDay_percent[i] = str(0.0) + "%"
        for i in range(32):
            try:
                self.missed_1stLevel_perDay_percent[i] = str(round(float(self.missed_1stLevel_perDay[i]) / self.total_perDay[i] * 100, 1)) + "%"
            except:
                self.missed_1stLevel_perDay_percent[i] = str(0.0) + "%"
        for i in range(32):
            try:
                self.answered_aa_perDay_percent[i] = str(round(float(self.answered_aa_perDay[i]) / self.total_perDay[i] * 100, 1)) + "%"
            except:
                self.answered_aa_perDay_percent[i] = str(0.0) + "%"

        for i in range(24):
            try:
                self.answered_1stLevel_perHour_percent[i] = str(round(float(self.answered_1stLevel_perHour[i]) / self.total_perHour[i] * 100, 1)) + "%"
            except:
                self.answered_1stLevel_perHour_percent[i] = str(0.0) + "%"
        for i in range(24):
            try:
                self.missed_1stLevel_perHour_percent[i] = str(round(float(self.missed_1stLevel_perHour[i]) / self.total_perHour[i] * 100, 1)) + "%"
            except:
                self.missed_1stLevel_perHour_percent[i] = str(0.0) + "%"
        for i in range(24):
            try:
                self.answered_aa_perHour_percent[i] = str(round(float(self.answered_aa_perHour[i]) / self.total_perHour[i] * 100, 1)) + "%"
            except:
                self.answered_aa_perHour_percent[i] = str(0.0) + "%"

    def create_csv_file(self, filename):

        f = open(filename, "w")
        f.write("lala")
        f.close()

###########################################################################################################################################
class ExtensionStats:
    def __init__(self, extension):
        self.extension = extension

        self.total = 0
        self.total_perDay = [0 for i in range(32)]
        self.total_perHour = [0 for i in range(24)]

        self.answered = 0
        self.answered_percent = 0
        self.answered_perDay = [0 for i in range(32)]
        self.answered_perDay_percent = [0 for i in range(32)]
        self.answered_perHour = [0 for i in range(24)]
        self.answered_perHour_percent = [0 for i in range(24)]

        self.missed = 0
        self.missed_percent = 0
        self.missed_perDay = [0 for i in range(32)]
        self.missed_perDay_percent = [0 for i in range(32)]
        self.missed_perHour = [0 for i in range(24)]
        self.missed_perHour_percent = [0 for i in range(24)]

        self.answered_vm = 0
        self.answered_vm_percent = 0
        self.answered_vm_perDay = [0 for i in range(32)]
        self.answered_vm_perDay_percent = [0 for i in range(32)]
        self.answered_vm_perHour = [0 for i in range(24)]
        self.answered_vm_perHour_percent = [0 for i in range(24)]

    def populate_percentages(self):

        for i in range(32):
            try:
                self.answered_perDay_percent[i] = str(round(float(self.answered_perDay[i]) / self.total_perDay[i] * 100, 1)) + "%"
            except:
                self.answered_perDay_percent[i] = str(0.0) + "%"
        for i in range(32):
            try:
                self.missed_perDay_percent[i] = str(round(float(self.missed_perDay[i]) / self.total_perDay[i] * 100, 1)) + "%"
            except:
                self.missed_perDay_percent[i] = str(0.0) + "%"
        for i in range(32):
            try:
                self.answered_vm_perDay_percent[i] = str(round(float(self.answered_vm_perDay[i]) / self.total_perDay[i] * 100, 1)) + "%"
            except:
                self.answered_vm_perDay_percent[i] = str(0.0) + "%"

        for i in range(24):
            try:
                self.answered_perHour_percent[i] = str(round(float(self.answered_perHour[i]) / self.total_perHour[i] * 100, 1)) + "%"
            except:
                self.answered_perHour_percent[i] = str(0.0) + "%"
        for i in range(24):
            try:
                self.missed_perHour_percent[i] = str(round(float(self.missed_perHour[i]) / self.total_perHour[i] * 100, 1)) + "%"
            except:
                self.missed_perHour_percent[i] = str(0.0) + "%"
        for i in range(24):
            try:
                self.answered_vm_perHour_percent[i] = str(round(float(self.answered_vm_perHour[i]) / self.total_perHour[i] * 100, 1)) + "%"
            except:
                self.answered_vm_perHour_percent[i] = str(0.0) + "%"


    def __str__(self):
        return "\ntotal: {}\ntotal_perDay: {}\ntotal_perHour: {}" \
               "\n\nanswered_1stLevel: {}" \
               "\nanswered_perDay: {}\nanswered_perDay_percent: {}" \
               "\nanswered_perHour: {}\nanswered_perHour_percent: {}" \
               "\n\nmissed_1stLevel: {}" \
               "\nmissed_perDay: {}\nmissed_perDay_percent: {}" \
               "\nmissed_perHour: {}\nmissed_perHour_percent: {}" \
               "\n\nanswered_aa: {}" \
               "\nanswered_aa_perDay: {}\nanswered_aa_perDay_percent: {}" \
               "\nanswered_aa_perHour: {}\nanswered_aa_perHour_percent: {}".format(
            self.total, self.total_perDay, self.total_perHour,
            self.answered,
            self.answered_perDay, self.answered_perDay_percent,
            self.answered_perHour, self.answered_perHour_percent,
            self.missed,
            self.missed_perDay, self.missed_perDay_percent,
            self.missed_perHour, self.missed_perHour_percent,
            self.answered_vm,
            self.answered_vm_perDay, self.answered_vm_perDay_percent,
            self.answered_vm_perHour, self.answered_vm_perHour_percent)


###########################################################################################################################################
class HuntPilotStats:
    def __init__(self, huntpilot):
        self.huntpilot = huntpilot

        self.total = 0
        self.total_perDay = [0 for i in range(32)]
        self.total_perHour = [0 for i in range(24)]

        self.answered = 0
        self.answered_percent = 0
        self.answered_perDay = [0 for i in range(32)]
        self.answered_perDay_percent = [0 for i in range(32)]
        self.answered_perHour = [0 for i in range(24)]
        self.answered_perHour_percent = [0 for i in range(24)]

        self.missed = 0
        self.missed_percent = 0
        self.missed_perDay = [0 for i in range(32)]
        self.missed_perDay_percent = [0 for i in range(32)]
        self.missed_perHour = [0 for i in range(24)]
        self.missed_perHour_percent = [0 for i in range(24)]

        self.answered_vm = 0
        self.answered_vm_percent = 0
        self.answered_vm_perDay = [0 for i in range(32)]
        self.answered_vm_perDay_percent = [0 for i in range(32)]
        self.answered_vm_perHour = [0 for i in range(24)]
        self.answered_vm_perHour_percent = [0 for i in range(24)]

        self.answeredBy = {}

    def populate_percentages(self):

        for i in range(32):
            try:
                self.answered_perDay_percent[i] = str(round(float(self.answered_perDay[i]) / self.total_perDay[i] * 100, 1)) + "%"
            except:
                self.answered_perDay_percent[i] = str(0.0) + "%"
        for i in range(32):
            try:
                self.missed_perDay_percent[i] = str(round(float(self.missed_perDay[i]) / self.total_perDay[i] * 100, 1)) + "%"
            except:
                self.missed_perDay_percent[i] = str(0.0) + "%"
        for i in range(32):
            try:
                self.answered_vm_perDay_percent[i] = str(round(float(self.answered_vm_perDay[i]) / self.total_perDay[i] * 100, 1)) + "%"
            except:
                self.answered_vm_perDay_percent[i] = str(0.0) + "%"

        for i in range(24):
            try:
                self.answered_perHour_percent[i] = str(round(float(self.answered_perHour[i]) / self.total_perHour[i] * 100, 1)) + "%"
            except:
                self.answered_perHour_percent[i] = str(0.0) + "%"
        for i in range(24):
            try:
                self.missed_perHour_percent[i] = str(round(float(self.missed_perHour[i]) / self.total_perHour[i] * 100, 1)) + "%"
            except:
                self.missed_perHour_percent[i] = str(0.0) + "%"
        for i in range(24):
            try:
                self.answered_vm_perHour_percent[i] = str(round(float(self.answered_vm_perHour[i]) / self.total_perHour[i] * 100, 1)) + "%"
            except:
                self.answered_vm_perHour_percent[i] = str(0.0) + "%"


    def __str__(self):
        return "\ntotal: {}\ntotal_perDay: {}\ntotal_perHour: {}" \
               "\n\nanswered: {}" \
               "\nanswered_perDay: {}\nanswered_perDay_percent: {}" \
               "\nanswered_perHour: {}\nanswered_perHour_percent: {}" \
               "\n\nmissed: {}" \
               "\nmissed_perDay: {}\nmissed_perDay_percent: {}" \
               "\nmissed_perHour: {}\nmissed_perHour_percent: {}" \
               "\n\nanswered_vm: {}" \
               "\nanswered_vm_perDay: {}\nanswered_vm_perDay_percent: {}" \
               "\nanswered_vm_perHour: {}\nanswered_vm_perHour_percent: {}" \
               "\n\nansweredBy: {}".format(
            self.total, self.total_perDay, self.total_perHour,
            self.answered,
            self.answered_perDay, self.answered_perDay_percent,
            self.answered_perHour, self.answered_perHour_percent,
            self.missed,
            self.missed_perDay, self.missed_perDay_percent,
            self.missed_perHour, self.missed_perHour_percent,
            self.answered_vm,
            self.answered_vm_perDay, self.answered_vm_perDay_percent,
            self.answered_vm_perHour, self.answered_vm_perHour_percent,
            self.answeredBy)

###########################################################################################################################################
