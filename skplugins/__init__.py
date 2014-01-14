#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__ = 'Bruno Adelé <bruno@adele.im>'
__copyright__ = 'Copyright (C) 2013 Bruno Adelé'
__description__ = """A plugins for serialkiller project"""
__license__ = 'GPL'
__version__ = '0.0.1'

import requests

class skplugins(object):
    """Generic Class for type"""
    def __init__(self, **kwargs):

        # Set parameters
        self._params = kwargs
        self._results = dict()
        self._types = dict()

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
        if 'result' not in self.results:
            return None
        else:
            return self.results['result']

    @property
    def results(self):
        """Get Value"""
        return self._results

    @property
    def type(self):
        if 'result' not in self._types:
            raise Exception("type not found for result")

        return self._types['result']

    @property
    def types(self):
        return self._types

    def check(self):
        """Check Sensor"""
        mess = "%s.%s" % (self.__class__, sys._getframe().f_code.co_name)
        raise NotImplementedError(mess)


def addValuePlugin(server, sensorid, plugin):
    "Add value from plugin"""
    addValue(server, sensorid, plugin.type, plugin.result)


def addEventPlugin(server, sensorid, plugin):
    "Add event from plugin"""
    addEvent(server, sensorid, plugin.type, plugin.result)


def addValue(server, sensorid, type, value):
    "Add value from value"""
    url = 'http://%(server)s/addValue/%(sensorid)s/%(type)s/%(value)s' % locals()
    print url
    requests.get(url)


def addEvent(server, sensorid, type, value):
    "Add event from value"""
    url = 'http://%(server)s/addValue/%(sensorid)s/%(type)s/%(value)s' % locals()
    print url
    requests.get(url)
