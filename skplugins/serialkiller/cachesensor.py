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

import os
import json


class cachesensor(object):
    """Cache sensors"""
    def __init__(self, **kwargs):
        self._cachefile = None

        if 'cachefile' in kwargs:
            self._cachefile = kwargs['cachefile']

    def openJSON(self):
        if self._cachefile is None:
            return None

        if not os.path.exists(self._cachefile):
            return None

        lines = open(self._cachefile).read()
        return json.loads(lines)

    def saveJSON(self, jsoncontent):
        if self._cachefile is None:
            return

        with open(self._cachefile, 'w') as f:
            jsontext = json.dumps(
                jsoncontent, sort_keys=True,
                indent=4, separators=(',', ': ')
            )
            f.write(jsontext)
            f.close()


    def getValue(self, sensorid):
        sensors = self.openJSON()

        if sensors is None or sensorid not in sensors:
            return None

        return sensors[sensorid]

    def setValue(self, sensorid, value):
        sensors = self.openJSON()

        if sensors is None:
            sensors = dict()

        if sensorid not in sensors:
            sensors[sensorid] = dict()

        sensors[sensorid] = {'value': value}
        self.saveJSON(sensors)


