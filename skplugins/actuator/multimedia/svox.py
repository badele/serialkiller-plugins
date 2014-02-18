#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__ = 'Bruno Adelé <bruno@adele.im>'
__copyright__ = 'Copyright (C) 2013 Bruno Adelé'
__description__ = """A plugins for serialkiller project"""
__license__ = 'GPL'
__version__ = '0.0.2'

from subprocess import *
from skplugins.actuator import actuator


class svox(actuator):
    """Use svox-pico Text To Speech"""
    def __init__(self, **kwargs):
        super(svox, self).__init__(**kwargs)

    def action(self, mess):
        cmd = 'pico2wave -l fr-FR -w /tmp/test.wav "%s" ; aplay /tmp/test.wav' % mess
        Popen(cmd, shell=True)