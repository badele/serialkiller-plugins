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
import requests
import time
import threading
import logging

from collections import defaultdict


class daemon(threading.Thread):
    """Generic Class for type"""
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self._stopevent = threading.Event( )

        # Set parameters
        self._params = kwargs
        self._params['threadwait'] = 2

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
        if 'result' not in self.results:
            return None
        else:
            return self.results['result']

    @property
    def results(self):
        """Get Value"""
        return self._results

    @results.setter
    def results(self, value):
        """Set Value"""
        self._results = value

    @property
    def type(self):
        if 'result' not in self._types:
            raise Exception("type not found for result")

        return self._types['result']

    @property
    def types(self):
        return self._types

    def stop(self):
        self._stopevent.set( )

    def run(self):
        """Check Sensor"""
        # noinspection PyProtectedMember
        mess = "%s.%s" % (self.__class__, sys._getframe().f_code.co_name)
        raise NotImplementedError(mess)

