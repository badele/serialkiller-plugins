#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__ = 'Bruno Adelé <bruno@adele.im>'
__copyright__ = 'Copyright (C) 2013 Bruno Adelé'
__description__ = """A plugins for serialkiller project"""
__license__ = 'GPL'
__version__ = '0.0.2'

# On the server require mochad application

import re
import os
import socket
from collections import defaultdict

from skplugins.daemon import daemon

class x10(daemon):
    """Check the x10 status"""
    def __init__(self, **kwargs):
        super(x10, self).__init__(**kwargs)
        self._types = {
            'result': None,
        }
        self.initPlugin()

    def initPlugin(self):
            self.results['result'] = defaultdict(lambda: None)

    def executeMochadCommand(self, command):
            if 'mochad' not in self.params:
                self.results['result'] = None
                return

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.params['mochad'], 1099))
            s.sendall("%s\n" % command)
            s.shutdown(socket.SHUT_WR)

            out = ''
            while 1:
                data = s.recv(128)
                out += data

                if data == '':
                    break

            s.close()
            return out

    def checkStatus(self):

            out = self.executeMochadCommand('st')
            results = re.findall(r'House ([A-O]): ([0-9A-F]=.*)', out)
            if results:
                for r in results:
                    x10house = r[0]
                    x10sensors = r[1].split(',')

                    for x10sensor in x10sensors:
                        (sensorid, value) = x10sensor.split('=')
                        self.results['result']["%s%s" % (x10house, sensorid)] = int(value)

    def power(self,unit, value):
            self.executeMochadCommand('pl %s %s' % (unit, value))

    def run(self):

        # Loop mochad content
        while not self._stopevent.isSet():

            self.checkStatus()

            self._stopevent.wait(self.params['threadwait'])