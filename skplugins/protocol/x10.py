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
import os
import socket

from skplugins import skplugins

class x10(skplugins):
    """Check the x10 status"""
    def __init__(self, **kwargs):
        super(x10, self).__init__(**kwargs)
        self._types = {
            'result': None,
        }
        self.check()

    @property
    def params(self):
        """Get Value"""
        return self._params

    @params.setter
    def params(self, value):
        self._params = value

    def check(self):

        if 'mochad' not in self.params:
            self.results['result'] = None
            return

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.params['mochad'], 1099))
        s.sendall("st\n")
        s.shutdown(socket.SHUT_WR)

        out = ''
        while 1:
            data = s.recv(1024)
            if data == '':
                break

            out += data

        s.close()

        self.results['result'] =dict()
        results = re.findall(r'House ([A-O]): ([0-9A-F]=.*)', out)
        if results:
            for r in results:
                x10house = r[0]
                x10sensors = r[1].split(',')

                for x10sensor in x10sensors:
                    (sensorid, value) = x10sensor.split('=')
                    self.results['result']["%s%s" % (x10house, sensorid)] = value
