import time


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

