from twisted.trial.unittest import TestCase
from datetime import datetime

from schedule import Schedule

class ScheduleTests(TestCase):

    def setUp(self):
        self.schedule = Schedule('1 0 * * *',
                                 datetime(2012, 10, 20, 10, 20, 34))

    def test_getnext(self):
        now = datetime(2013, 6, 20, 10, 20, 34)
        print self.schedule.get_next_seconds(now)

