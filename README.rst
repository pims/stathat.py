stathat.py
==========

A minimalistic API wrapper for StatHat.com, powered by Requests.

Usage::

    >>> from stathat import StatHat
    >>> stats = StatHat('me@kennethreitz.com')
    >>> stats.count('wtfs/minute', 10)
    True
    >>> stats.value('connections.active', 85092)
    True

Enjoy.


Batch usage::

    >>> from stathat import StatHat
    >>> stats = StatHat('xxxxxxxx', buffer_size=10)
    >>> stats.add('count', 'wtfs/minute', 10) # will buffer
    >>> stats.add('value', 'connections.active', 85092)
    >>> stats.flush() # optional, happens automatically when buffer_size is reached

Installation
------------

Installation is simple::

    $ pip install git+git://github.com/pims/stathat.py.git
