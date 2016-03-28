"""
Represents a recurring schedule
"""

from croniter import croniter
from datetime import datetime

class Schedule(object):

    def __init__(self, cronentry, start=None):
        self.croniter = croniter(cronentry, start or datetime.now())
        self.cronentry = cronentry

    def to_dict(self):
        """
        Used to convert to JSON format
        """
        return {"cron": self.cronentry}

    @staticmethod
    def from_dict(dictionary):
        return Schedule(dictionary['cron'])

    def get_next_seconds(self, now=None):
        """
        Get the number of seconds between now and next date of occurrence
        """
        now = now or datetime.now()
        later = datetime.min
        while later < now:
            later = self.croniter.get_next(ret_type=datetime)
        return (later - now).total_seconds()


