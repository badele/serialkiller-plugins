#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__ = 'Bruno Adelé <bruno@adele.im>'
__copyright__ = 'Copyright (C) 2013 Bruno Adelé'
__description__ = """A plugins for serialkiller project"""
__license__ = 'GPL'
__version__ = '0.0.2'

from skplugins.checker import checker


class myip(checker):
    """Check your public IP"""
    def __init__(self, **kwargs):
        super(myip, self).__init__(**kwargs)
        self._types = {
            'result': 'ulong',
        }
        self.check()

    def IP2Int(self, ip):
        o = map(int, ip.split('.'))
        res = (16777216 * o[0]) + (65536 * o[1]) + (256 * o[2]) + o[3]
        return res


    def check(self):

        r = self.getUrl("http://www.telize.com/ip")
        if r.status_code != 200:
            return None

        self.results['result'] = self.IP2Int(r.content)