#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__ = 'Bruno Adelé <bruno@adele.im>'
__copyright__ = 'Copyright (C) 2013 Bruno Adelé'
__description__ = """A plugins for serialkiller project"""
__license__ = 'GPL'
__version__ = '0.0.1'


import os
import __main__


from skplugins import addValuePlugin, addEventPlugin, addValue, addEvent
from skplugins.network.ping import ping
from skplugins.energy.teleinfo import teleinfo
from skplugins.weather.sunshine import sunshine


def isOnlyInstance():
    """Check if one instance"""
    return os.system("(( $(ps -ef | grep python | grep '[" +
                     __main__.__file__[0] + "]" + __main__.__file__[1:] +
                     "' | wc -l) > 1 ))") != 0

if isOnlyInstance():
    server = '192.168.253.35'

    # Check internet connexion
    # result = ping(destination="8.8.8.8", count=1)
    # addValuePlugin(server, 'hp2012:network:online', result)

    # Check teleinfo informations
    # result = teleinfo(dev='/dev/teleinfo')
    # addValue(server, 'domsrv:teleinfo:hchc', result.types['HCHC'], result.results['HCHC'])
    # addValue(server, 'domsrv:teleinfo:hchp', result.types['HCHP'], result.results['HCHP'])
    # addValue(server, 'domsrv:teleinfo:iinst', result.types['IINST'], result.results['IINST'])
    # addValue(server, 'domsrv:teleinfo:imax', result.types['IMAX'], result.results['IMAX'])
    # addValue(server, 'domsrv:teleinfo:isousc', result.types['ISOUSC'], result.results['ISOUSC'])
    # addValue(server, 'domsrv:teleinfo:papp', result.types['PAPP'], result.results['PAPP'])

    # Check night
    result = sunshine(latitude="43:36:43", longitude="3:53:38", elevation=8)
    addValuePlugin(server, 'domsrv:weather:sunshine', result)
