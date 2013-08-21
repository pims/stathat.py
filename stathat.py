# -*- coding: utf-8 -*-
import requests
import time
try:
    import json
except ImportError, err:
    import simplejson as json

"""
stathat.py
~~~~~~~~~~

A minimalistic API wrapper for StatHat.com, powered by Requests.

Usage::

    >>> from stathat import StatHat
    >>> stats = StatHat('me@kennethreitz.com')
    >>> stats.count('wtfs/minute', 10)
    True
    >>> stats.count('connections.active', 85092)
    True

Enjoy.


New support for batch:

{
    "ezkey": "XXXYYYZZZ",
    "data": [
        {"stat": "page view", "count": 2},
        {"stat": "messages sent~total,female,europe", "count": 1},
        {"stat": "request time~total,messages", "value": 23.094},
        {"stat": "ws0: load average", "value": 0.732, "t": 1363118126},
    ]
}

"""

DEFAULT_STATHAT_URL = 'https://api.stathat.com'



class StatHat(object):
    """The StatHat API wrapper."""

    STATHAT_URL = DEFAULT_STATHAT_URL
    STATHAT_CMD_COUNT = 'count'
    STATHAT_CMD_VALUE = 'value'

    def __init__(self, ezkey=None, **kwargs):
        self.ezkey = ezkey

        # Enable keep-alive and connection-pooling.
        self.session = requests.session()
        self.buffer = []
        self.buffer_len = 0

        self.prefix = kwargs.pop('prefix','')
        self.buffer_size = int(kwargs.pop('buffer_size', 100))
        self.logger = kwargs.pop('logger', None)

    def _log(self, *args):
        '''Forwards arguments to logger (debug) if available'''
        if self.logger is not None:
            self.logger.debug(*args)

    def _key(self, key):
        '''Prepends prefix if applicable

        param: key: stats key
        type: key: str
        rtype: str
        '''
        return self.prefix + '.' + key if self.prefix else key

    def add(self, cmd, key, value, t=None, flush=False):
        '''Adds event to buffer and flush buffer when buffer size > limit

        param: cmd: stats command either 'count' or 'value'
        type: cmd: str

        param: key: stats key
        type: key: str

        param: value: value or count
        type: value: int

        param: t: timestamp of the event
        type: t: int

        param: flush: whether buffer should be flushed immediately
        type: flush: bool

        rtype: bool
        '''

        t = int(time.time()) if t is None else t
        data = {
            'stat' : self._key(key),
            cmd : value, 
            't' : t,
        }

        self.buffer.append(data)
        self.buffer_len += 1

        if flush or self.buffer_len > self.buffer_size:
            self._log("Flushing: %s", self.buffer)
            req = self._http_post('/ez', self.buffer)
            return req.ok
        return True

    def _http_post(self, path, data):
        '''Sends post request to stathat API.
        Requests are batched and json encoded

        param: path: stathat API path, should be /ez
        type: path: str
        
        param: data: list of events (dicts)
        type: data: list

        rtype: requests.Response
        '''
        url = self.STATHAT_URL + path
        envelope = {'ezkey': self.ezkey, 'data' : data}

        req = self.session.post(url, 
            data=json.dumps(envelope),
            headers={'Content-type': 'application/json'})
        if req.ok:
            self.buffer = []
            self.buffer_len = 0
        return req

    def value(self, key, value, t=None):
        '''Sends value events immediately to stathat API 
        
        param: key: stats key
        type: key: str
        
        param: value: value associated to the key
        type: value: int

        param: t: optional UTC timestamp
        type: t: int

        rtype: bool
        '''
        return self.add(self.STATHAT_CMD_VALUE, key, value, t=t, flush=True)

    def count(self, key, count, t=None):
        '''Sends count events to stathat API 
        
        param: key: stats key
        type: key: str
        
        param: count: count associated to the key
        type: count: int

        param: t: optional UTC timestamp
        type: t: int
        
        rtype: bool
        '''
        return self.add(self.STATHAT_CMD_COUNT, key, count, t=t, flush=True)
        
    def flush(self):
        '''Flushes the buffer to stathat API
        
        rtype: bool
        '''
        self._log("Flushing: %s", self.buffer)
        r = self._http_post('/ez', self.buffer)
        return r.ok
