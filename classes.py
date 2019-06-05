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

