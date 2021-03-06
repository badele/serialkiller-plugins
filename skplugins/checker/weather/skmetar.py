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
from skplugins.checker import checker

from metar import Metar


class skmetar(checker):
    """Check the metar information"""
    def __init__(self, **kwargs):
        super(skmetar, self).__init__(**kwargs)
        self._types = {
            'temp': 'skfloat',
            'dewpt': 'skfloat',
            'pressure': 'skfloat',
            'wind_speed': 'skfloat',
            'humidity': 'skfloat',
            'wind_chill': 'skfloat',
            'visibility': 'ushort'
        }
        self.check()

    def check(self):
        if 'station' not in self.params:
            self.results['result'] = None
            return

        results = None
        try:
            results = self.getcachedresults()
        except:
            self.log.exception('error in getcachedresults function')
            raise

        if results:
            # Result in the cache
            self.results = results
            return

        # Get Metar information
        r = None
        try:
            r = self.getUrl("http://weather.noaa.gov/pub/data/observations/metar/stations/%s.TXT" % self.params['station'])
        except:
            self.log.exception('error in getUrl function')
            raise

        if r is None or r.status_code != 200:
            return None

        # Extract only Metar informations
        m = re.search(
            '%s .*' % self.params['station'],
            r.content
        )

        if not m:
            return

        # Decode metar informations
        code = m.group(0)
        decode = Metar.Metar(code)

        # Get temperature
        if decode.temp:
            self.results['temp'] = decode.temp.value()

        # Get dewpt temperature
        if decode.dewpt:
            self.results['dewpt'] = decode.dewpt.value()

        # Get pressure
        if decode.press:
            self.results['pressure'] = decode.press.value()

        # Visibility
        if decode.vis:
            self.results['visibility'] = int(decode.vis.value())

        # Get wind speed
        if decode.wind_speed:
            self.results['wind_speed'] = decode.wind_speed.value() * 1.852

        # Calculate the relative humidity
        if decode.temp and decode.dewpt:
            temp = decode.temp.value()
            dewpt = decode.dewpt.value()
            self.results['humidity'] = round(100 * ((112 - 0.1 * temp + dewpt) / (112 + 0.9 * temp))**8, 2)

        # Calculate the wind chill or heat index
        if decode.temp and decode.wind_speed:
            speed = decode.wind_speed.value() * 1.852
            temp = decode.temp.value()
            self.results['wind_chill'] = round(13.12 + 0.6215*temp + (0.3965*temp - 11.37) * speed ** 0.16, 2)

        # Save results
        self.setcacheresults()
