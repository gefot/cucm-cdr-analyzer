import time

    def __init__(self, department):
        self.department = department

        self.total = 0
        self.total_perDay = [0 for i in range(32)]
        self.total_perHour = [0 for i in range(24)]

        self.answered_1stLevel = 0
        self.answered_1stLevel_perDay = [0 for i in range(32)]
        self.answered_1stLevel_perHour = [0 for i in range(24)]

        self.missed_1stLevel = 0
        self.missed_1stLevel_perDay = [0 for i in range(32)]
        self.missed_1stLevel_perHour = [0 for i in range(24)]

        self.answered_aa = 0
        self.answered_aa_perDay = [0 for i in range(32)]
        self.answered_aa_perHour = [0 for i in range(24)]

        self.missed_aa = 0
        self.missed_aa_perDay = [0 for i in range(32)]
        self.missed_aa_perHour = [0 for i in range(24)]

    def __str__(self):
        return "\ntotal: {}\ntotal_perDay: {}\ntotal_perHour: {}" \
               "\n\nanswered_1stLevel: {}\nanswered_1stLevel_perDay: {}\nanswered_1stLevel_perHour: {}" \
               "\n\nmissed_1stLevel: {}\nmissed_1stLevel_perDay: {}\nmissed_1stLevel_perHour: {}" \
               "\n\nanswered_aa: {}\nanswered_aa_perDay: {}\nanswered_aa_perHour: {}" \
               "\n\nmissed_aa: {}\nmissed_aa_perDay: {}\nmissed_aa_perHour: {}".format(
            self.total, self.total_perDay, self.total_perHour,
            self.answered_1stLevel, self.answered_1stLevel_perDay, self.answered_1stLevel_perHour,
            self.missed_1stLevel, self.missed_1stLevel_perDay, self.missed_1stLevel_perHour,
            self.answered_aa, self.answered_aa_perDay, self.answered_aa_perHour,
            self.missed_aa, self.missed_aa_perDay, self.missed_aa_perHour)


###########################################################################################################################################
class ExtensionStats:
    def __init__(self, extension):
        self.extension = extension

        self.total = 0
        self.total_perDay = [0 for i in range(32)]
        self.total_perHour = [0 for i in range(24)]

        self.answered = 0
        self.answered_perDay = [0 for i in range(32)]
        self.answered_perHour = [0 for i in range(24)]

        self.missed = 0
        self.missed_perDay = [0 for i in range(32)]
        self.missed_perHour = [0 for i in range(24)]

        self.answered_vm = 0
        self.answered_vm_perDay = [0 for i in range(32)]
        self.answered_vm_perHour = [0 for i in range(24)]

        self.forwarded = 0
        self.forwarded_perDay = [0 for i in range(32)]
        self.forwarded_perHour = [0 for i in range(24)]

    def __str__(self):
        return "\ntotal: {}\ntotal_perDay: {}\ntotal_perHour: {}" \
               "\n\nanswered: {}\nanswered_perDay: {}\nanswered_perHour: {}" \
               "\n\nmissed: {}\nmissed_perDay: {}\nmissed_perHour: {}" \
               "\n\nanswered_vm: {}\nanswered_vm_perDay: {}\nanswered_vm_perHour: {}" \
               "\n\nforwarded: {}\nforwarded_perDay: {}\nforwarded_perHour: {}".format(
            self.total, self.total_perDay, self.total_perHour,
            self.answered, self.answered_perDay, self.answered_perHour,
            self.missed, self.missed_perDay, self.missed_perHour,
            self.answered_vm, self.answered_vm_perDay, self.answered_vm_perHour,
            self.forwarded, self.forwarded_perDay, self.forwarded_perHour)


###########################################################################################################################################
class HuntPilotStats:
    def __init__(self, huntpilot):
        self.huntpilot = huntpilot

        self.total = 0
        self.total_perDay = [0 for i in range(32)]
        self.total_perHour = [0 for i in range(24)]

        self.answered = 0
        self.answered_perDay = [0 for i in range(32)]
        self.answered_perHour = [0 for i in range(24)]

        self.missed = 0
        self.missed_perDay = [0 for i in range(32)]
        self.missed_perHour = [0 for i in range(24)]

        self.answered_vm = 0
        self.answered_vm_perDay = [0 for i in range(32)]
        self.answered_vm_perHour = [0 for i in range(24)]

        self.forwarded = 0
        self.forwarded_perDay = [0 for i in range(32)]
        self.forwarded_perHour = [0 for i in range(24)]

    def __str__(self):
        return "\ntotal: {}\ntotal_perDay: {}\ntotal_perHour: {}" \
               "\n\nanswered: {}\nanswered_perDay: {}\nanswered_perHour: {}" \
               "\n\nmissed: {}\nmissed_perDay: {}\nmissed_perHour: {}" \
               "\n\nanswered_vm: {}\nanswered_vm_perDay: {}\nanswered_vm_perHour: {}" \
               "\n\nforwarded: {}\nforwarded_perDay: {}\nforwarded_perHour: {}".format(
            self.total, self.total_perDay, self.total_perHour,
            self.answered, self.answered_perDay, self.answered_perHour,
            self.missed, self.missed_perDay, self.missed_perHour,
            self.answered_vm, self.answered_vm_perDay, self.answered_vm_perHour,
            self.forwarded, self.forwarded_perDay, self.forwarded_perHour)

###########################################################################################################################################
class CDRRecord:

    def __init__(self, global_id, date, calling_num, called_num, final_called_num, last_redirect_num, duration, origDeviceName, destDeviceName):
        self.global_id = global_id
        self.date = date
        self.calling_num = calling_num
        self.called_num = called_num
        self.final_called_num = final_called_num
        self.last_redirect_num = last_redirect_num
        self.duration = duration
        self.origDeviceName = origDeviceName
        self.destDeviceName = destDeviceName

    def __str__(self):
        return "{}, {}, {}, {}, {}, {}, {}, {}, {}".format(self.global_id, self.date, self.calling_num, self.called_num,
                                                           self.final_called_num, self.last_redirect_num,
                                                           time.strftime("%M:%S", time.gmtime(int(int(self.duration)))), self.origDeviceName, self.destDeviceName)


###########################################################################################################################################
class CategorizedCall:

    def __init__(self, call_type, handle):
        self.call_type = call_type
        self.handle = handle

        self.answered_by = "unknown"
        self.option = "unknown"

        self.cdr_record = "unknown"
        self.cdr_record_aa = "unknown"

    def __str__(self):
        return "{}, {}, {}, {}".format(self.call_type, self.handle, self.answered_by, self.option)


###########################################################################################################################################