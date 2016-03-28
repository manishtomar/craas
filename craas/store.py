"""
Jobs storage
"""

from uuid import uuid1

class MemStore(object):
    """
    Storage of jobs in memory
    """

    def __init__(self):
        self.jobs = {}

    def add_job(self, job):
        id = uuid1().hex
        # TODO: Not happy with putting id in like this. Need to think about it
        job.id = id
        self.jobs[id] = job
        return job

    def get_job(self, jobid):
        return self.jobs[jobid]


store = MemStore()

