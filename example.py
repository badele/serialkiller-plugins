#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

#from skplugins.checker.weather.skmetar import skmetar
from skplugins.checker.weather.sunshine import sunshine
#from skplugins.checker.weather.vigimeteo import vigimeteo

maxlen = 20

#################
# Check sunshine
#################
sunshinestxt = ["Night", "Astronomic", "Naval", "Civil", "Day"]

result = sunshine(latitude="43:36:43", longitude="3:53:38", elevation=8)
sun_alt = result.results["sun_alt"]
sun_az = result.results["sun_az"]
sun_idx = min(4, result.results["sunshine_idx"])
sun_idx_text = sunshinestxt[sun_idx]

print("%s: %s" % ("Sun altitude".ljust(maxlen), sun_alt))
print("%s: %s" % ("Sun azimut".ljust(maxlen), sun_az))
print("%s: %s" % ("Sun idx".ljust(maxlen), sun_idx))
print("%s: %s" % ("Sun idx text".ljust(maxlen), sun_idx_text))


# #################
# # Metar
# #################
# result = skmetar(cachefile='/tmp/metar_34.cache', station='LFMT')
#
#
# #################
# # Vigimeteo
# #################
# result = vigimeteo(cachefile='/tmp/vigimeteo_34.cache', dep=34)
# print (result.results)