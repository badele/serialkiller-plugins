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
from collections import defaultdict

class actuator(object):
    """Generic Class for actuator object"""
    def __init__(self, **kwargs):

        # Set parameters
        self._params = kwargs

    @property
    def params(self):
        """Get Value"""
        return self._params

    @params.setter
    def params(self, value):
        self._params = value