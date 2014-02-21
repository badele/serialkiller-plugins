#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__ = 'Bruno Adelé <bruno@adele.im>'
__copyright__ = 'Copyright (C) 2013 Bruno Adelé'
__description__ = """A plugins for serialkiller project"""
__license__ = 'GPL'
__version__ = '0.0.2'

# Require python-metar library
# git clone https://github.com/tomp/python-metar.git
# cd python-metar
# python setup.py install

import re
import json
from skplugins.checker import checker


class sensor(checker):
    """Check the serialkiller server information"""
    def __init__(self, **kwargs):
        super(sensor, self).__init__(**kwargs)
        self._types = {
            'result': None,
        }
        self.check()

    def check(self):
        if 'server' not in self.params or 'sensorid' not in self.params:
            self.results['result'] = None
            return

        # Get Metar information
        url = "http://%s/api/1.0/sensor/%s/last" % (self.params['server'], self.params['sensorid'])
        r = self.getUrl(url)
        if r.status_code != 200:
            return None

        self.results = json.loads(r.content)