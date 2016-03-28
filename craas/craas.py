#!/usr/bin/env python

from functools import wraps

from twisted.internet import defer
from klein import Klein, run, route
import json

from job import Job, schedule_job
from store import store


def with_resource(cls):
    def decorator(f):
        def _wrap(self, request, *args, **kwargs):
            print 'wr_wrap', self, request, args
            request.content.seek(0)
            data = json.loads(request.content.read())
            resource = cls.from_dict(data)
            print 'got resource', resource
            return f(self, request, resource, *args, **kwargs)
        return _wrap
    return decorator

def returns_resource(f):
    print 'ret res', f
    @wraps(f)
    def _wrap(self, request, *args, **kwargs):
        print 'in _wrap', _wrap, f, request, args
        resource = f(self, request, *args, **kwargs)
        return json.dumps(resource.to_dict())
    print '_wrap', _wrap
    return _wrap


class JobsREST(object):

    app = Klein()

    def __init__(self):
        self.store = store

    @app.route('/jobs', methods=['POST'])
    @with_resource(Job) #@returns_resource
    @returns_resource
    def create_job(self, request, job):
        #print 'job to create', job
        job = self.store.add_job(job)
        schedule_job(job)
        return job

    @app.route('/job/<string:jobid>', methods=['GET'])
    @returns_resource # TODO: Find out why
    def get_job(self, request, jobid):
        #return json.dumps(store.get_job(jobid).to_dict())
        return store.get_job(jobid)

#print [type(r.endpoint) for r in JobsREST.app.url_map.iter_rules()]
JobsREST().app.run('localhost', 8000)
