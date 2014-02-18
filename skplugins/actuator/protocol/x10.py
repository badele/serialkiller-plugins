#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__ = 'Bruno Adelé <bruno@adele.im>'
__copyright__ = 'Copyright (C) 2013 Bruno Adelé'
__description__ = """A plugins for serialkiller project"""
__license__ = 'GPL'
__version__ = '0.0.2'

# On the server require mochad application

import socket
from skplugins.actuator import actuator


class x10(actuator):
    """Check the x10 status"""
    def __init__(self, **kwargs):
        super(x10, self).__init__(**kwargs)

    def action(self, sensorid, value):
        if 'mochad' not in self.params:
            self.results['result'] = None
            return

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.params['mochad'], 1099))
        s.sendall("pl %s %s\n" % (sensorid, value))
        s.shutdown(socket.SHUT_WR)
