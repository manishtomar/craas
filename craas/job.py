from __future__ import print_function

"""
Job class
"""

from functools import partial

from twisted.internet import reactor

from schedule import Schedule

class Job(object):
    """
    Long running job that runs at specific times in future
    """

    def __init__(self, schedule, webhook, id=None):
        self.schedule = schedule
        self.webhook = webhook
        self.id = id

    def to_dict(self):
        return { 'schedule': self.schedule.to_dict(),
                 'webhook': self.webhook,
                 'id': self.id
               }

    @staticmethod
    def from_dict(dictionary):
        return Job(Schedule.from_dict(dictionary['schedule']), dictionary['webhook'],
                   dictionary.get('id'))

    def __str__(self):
        return str(self.to_dict())


MAX_SCHEDULED_JOBS = 10
scheduled_jobs = {}

def schedule_job(job):
    seconds = job.schedule.get_next_seconds()
    caller = reactor.callLater(seconds, execute_job, job.id)
    scheduled_jobs[job.id] = caller, job.webhook
    print('job {} scheduled after {} seconds'.format(job.id, seconds))

def execute_job(jobid):
    d = treq.get(scheduled_jobs[jobid][1])
    d.addCallback(partial(print, 'webhook response\n'))
    schedule_job(store.get_job(jobid))


