import datetime


class Bell:
    def __init__(self, time_begin: datetime.time, time_end: datetime.time, number: int = None):
        self.number = number
        self.begin = time_begin
        self.end = time_end
