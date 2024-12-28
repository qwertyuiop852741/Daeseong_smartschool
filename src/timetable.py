import pycomcigan as pc
import config

class TimeTable:
    def __init__(self):
        self.timetable = pc.TimeTable(config.SCHOOL_NAME, week_num=0)
        print(self.timetable.timetable)

tt = TimeTable()
