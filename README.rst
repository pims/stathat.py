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


Options usage::
    
    >>> import logging
    >>> from stathat import StatHat
    >>> logging.config.fileConfig('config/logging.cfg')
    >>> logger = logging.getLogger("stats")
    >>> 
    >>> stats = StatHat('xxxxxxxx', buffer_size=100, logger=logger, prefix='prod')
    >>> stats.count('wtfs/minute', 10)
    
    2013-08-20 19:10:08,484 - stats - DEBUG - [{'count': 1, 'stat': 'prod.wtfs/minute', 't': 1377050997}]
    
    
Installation
------------

Installation is simple::

    $ pip install git+git://github.com/pims/stathat.py.git
