#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__ = 'Bruno Adelé <bruno@adele.im>'
__copyright__ = 'Copyright (C) 2013 Bruno Adelé'
__description__ = """A plugins for serialkiller project"""
__license__ = 'GPL'
__version__ = '0.0.2'
__apiversion__ = '1.0'

import os
import sys
import json
import time
import logging
import requests

from collections import defaultdict


class checker(object):
    """Generic Class for type"""
    def __init__(self, **kwargs):

        # Set parameters
        self._params = kwargs

        # Create logger
        self._params['logfile'] = '/tmp/%s.%s.log' % (self.__module__, self.__class__.__name__)
        self.log = logging.getLogger(self._params['logfile'])
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
        # Configure filehandler
        file_handler = logging.FileHandler(self._params['logfile'])
        file_handler.setFormatter(formatter)
        self.log.addHandler(file_handler)
        self.log.setLevel(logging.DEBUG)

        # Init result dict
        self._results = defaultdict(lambda: None)
        self._types = dict()

    def __del__(self):
        # Release log handlers
        handlers = self.log.handlers[:]
        for handler in handlers:
            handler.close()
            self.log.removeHandler(handler)

    # Get dynamically property
    def __getattr__(self, attr):
        if attr in self._results:
            return self._results[attr]
        else:
            return None

    @property
    def params(self):
        """Get Value"""
        return self._params

    @params.setter
    def params(self, value):
        self._params = value

    @property
    def result(self):
        """Get Value"""
        if  'default' not in self.results:
            mess = "%s.%s" % (self.__class__, sys._getframe().f_code.co_name)
            raise NotImplementedError(mess)
        else:
            return self.results[self.default]

    @property
    def results(self):
        """Get Value"""
        return self._results

    @results.setter
    def results(self, value):
        """Set Value"""
        self._results = value

    @property
    def default(self):
        if 'default' not in self._results:
            return None

        return self._results['default']

    @property
    def type(self):
        return 'text'
        if self.default not in self._types:
            raise Exception("type not found for %s" % self.default)

        return self._types[self.default]

    @property
    def types(self):
        return self._types

    def check(self):
        """Check Sensor"""
        # noinspection PyProtectedMember
        mess = "%s.%s" % (self.__class__, sys._getframe().f_code.co_name)
        raise NotImplementedError(mess)

    def getUrl(self, url):
        return requests.get(url)

    def getcachedresults(self):
        if 'cachefile' not in self.params:
            raise Exception("Not cachefile set")

        filename = self.params['cachefile']
        if 'cachetime' in self.params:
            cachetime = self.params['cachetime']
        else:
            cachetime = 1200

        if not os.path.exists(filename):
            # Cache not exists
            return None

        # Check if i use the cache results
        mtime = os.stat(filename).st_mtime
        now = time.time()
        if (now - mtime) > cachetime:
            # Cache is old
            return None

        # Use the cache file
        lines = open(filename).read()
        results = json.loads(lines)

        return results

    def setcacheresults(self):
        if 'cachefile' not in self.params:
            raise Exception("Not cachefile set")

        filename = self.params['cachefile']
        with open(filename, 'w') as f:
            jsontext = json.dumps(
                self.results, sort_keys=True,
                indent=4, separators=(',', ': ')
            )
            f.write(jsontext)
            f.close()


def addValuePlugin(server, sensorid, plugin):
    "Add value from plugin"""
    addValue(server, sensorid, plugin.type, plugin.result)


def addEventPlugin(server, sensorid, plugin):
    "Add event from plugin"""
    addEvent(server, sensorid, plugin.type, plugin.result)


def addValue(server, sensorid, ptype, value):
    "Add value from value"""
    if value is not None:
        url = 'sensor/%(sensorid)s/addValue/%(ptype)s/value=%(value)s' % locals()
        sendRequest(server, url)


def addEvent(server, sensorid, ptype, value):
    "Add event from value"""
    if value is not None:
        url = 'sensor/%(sensorid)s/addEvent/%(ptype)s/value=%(value)s' % locals()
        sendRequest(server, url)


def sendRequest(server, request):
    apiversion = __apiversion__
    try:
        apiversion = __apiversion__
        url = "http://%(server)s/api/%(apiversion)s/%(request)s" % locals()
        requests.get(url)
        #print url
    except:
        pass
