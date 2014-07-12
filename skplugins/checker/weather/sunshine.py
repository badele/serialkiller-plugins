#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import ephem
import math

from skplugins.checker import checker


class sunshine(checker):
    """Check if day or night"""
    def __init__(self, **kwargs):
        super(sunshine, self).__init__(**kwargs)
        self.results['default'] = 'sunshine_idx'
        self._types = {
            self.default: 'byte',
        }
        self.check()

    def check(self):

        # Consts
        HORIZON_STANDARD = "-0.833"
        HORIZON_CIVIL = "-6"
        HORIZON_NAVAL = "-12"
        HORIZON_ASTRO = "-18"

        # Select datetime
        if 'datetime' not in self.params:
            pdate = ephem.now()
            self.results['selected_time'] = ephem.localtime(pdate)
        else:
            pdate = ephem.Date(self.params['datetime'])
            self.results['selected_time'] = pdate

        self.results['selected_time_ts'] = int(time.mktime(pdate.datetime().timetuple()))

        # Elevation
        if 'elevation' not in self.params:
            self.params['elevation'] = 0

        # Observer horizon
        if 'horizon_std' not in self.params:
            self.params['horizon_std'] = HORIZON_STANDARD

        if 'horizon_civ' not in self.params:
            self.params['horizon_civ'] = HORIZON_CIVIL

        if 'horizon_nav' not in self.params:
            self.params['horizon_nav'] = HORIZON_NAVAL

        if 'horizon_ast' not in self.params:
            self.params['horizon_ast'] = HORIZON_ASTRO


        # Observer details
        obs = ephem.Observer()
        obs.lat = self.params['latitude']
        obs.long = self.params['longitude']
        obs.elevation = int(self.params['elevation'])
        obs.date = pdate

        # The sun
        sun=ephem.Sun(obs)
        sun.compute(obs)

        # Sun position
        self.results['sun_alt'] = int(sun.alt * 180 / math.pi)
        self.results['sun_ez'] = int(sun.az * 180 / math.pi)

        # Calc transit sun
        nexttransit = obs.next_transit(sun)
        prevtransit = obs.previous_transit(sun)

        if pdate.datetime().date() == nexttransit.datetime().date():
            obs.date = nexttransit

        if pdate.datetime().date() == prevtransit.datetime().date():
            obs.date = prevtransit

        # Standard
        obs.horizon = self.params['horizon_std']
        sunrise_std = obs.previous_rising(sun)
        sunset_std  = obs.next_setting(sun)
        self.results['sunrise_std'] = ephem.localtime(sunrise_std)
        self.results['sunset_std']  = ephem.localtime(sunset_std)
        self.results['sunrise_std_ts'] = int(time.mktime(obs.previous_rising(sun).datetime().timetuple()))
        self.results['sunset_std_ts']  = int(time.mktime(obs.next_setting(sun).datetime().timetuple()))

        # Civil
        obs.horizon = self.params['horizon_civ']
        sunrise_civ = obs.previous_rising(sun)
        sunset_civ  = obs.next_setting(sun)
        self.results['sunrise_civ'] = ephem.localtime(sunrise_civ)
        self.results['sunset_civ']  = ephem.localtime(sunset_civ)
        self.results['sunrise_civ_ts'] = int(time.mktime(obs.previous_rising(sun).datetime().timetuple()))
        self.results['sunset_civ_ts']  = int(time.mktime(obs.next_setting(sun).datetime().timetuple()))

        # Nav
        obs.horizon = self.params['horizon_nav']
        sunrise_nav = obs.previous_rising(sun)
        sunset_nav  = obs.next_setting(sun)
        self.results['sunrise_nav'] = ephem.localtime(sunrise_nav)
        self.results['sunset_nav']  = ephem.localtime(sunset_nav)
        self.results['sunrise_nav_ts'] = int(time.mktime(obs.previous_rising(sun).datetime().timetuple()))
        self.results['sunset_nav_ts']  = int(time.mktime(obs.next_setting(sun).datetime().timetuple()))

        # Astro
        obs.horizon = self.params['horizon_ast']
        sunrise_ast = obs.previous_rising(sun)
        sunset_ast  = obs.next_setting(sun)
        self.results['sunrise_ast'] = ephem.localtime(sunrise_ast)
        self.results['sunset_ast']  = ephem.localtime(sunset_ast)
        self.results['sunrise_ast_ts'] = int(time.mktime(obs.previous_rising(sun).datetime().timetuple()))
        self.results['sunset_ast_ts']  = int(time.mktime(obs.next_setting(sun).datetime().timetuple()))

        idx = -1
        if pdate < sunrise_ast or pdate > sunset_ast:
            # Night
            idx = 0

        if idx < 0 and (
                (pdate > sunrise_ast and pdate < sunrise_nav)
                or
                (pdate > sunset_nav and pdate < sunset_ast)
        ):
            # Astronomic
            idx = 1

        if idx < 0 and (
                (pdate > sunrise_nav and pdate < sunrise_civ)
                or
                (pdate > sunset_civ and pdate < sunset_nav)
        ):
            # Naval
            idx = 2

        if idx < 0 and (
                (pdate > sunrise_civ and pdate < sunrise_std)
                or
                (pdate > sunset_std and pdate < sunset_civ)
        ):
            # Civil
            idx = 3


        if idx < 0 and pdate > sunrise_std and pdate < sunset_std:
            # Day
            idx = 255

        self.results[self.default] = idx