#!/usr/bin/env python

import json, model, ephem, datetime, math
from housepy import config, log, net

log.info("////////// sun_watcher //////////")

"""
sudo pip install pyephem
(has a python3 compatible version too)

I want the presence of the sun, 0-1. which is not linear.
height from the horizon in degrees

sun.alt displays as degrees:minutes:seconds but acts as radians
max would be 90 which is 1.57
but civil twilight is -6 degrees, so take that into account

note that this will only hit 1.0 on the solstice

"""

try:
    observer = ephem.Observer()
    observer.lon = '-74.078021' # wave farm
    observer.lat = '42.318787'
    observer.elevation = 228 # m
    dt = datetime.datetime.utcnow()
    observer.date = dt.strftime("%Y/%m/%d %H:%M:%S")
    sun = ephem.Sun(observer)
    log.debug(sun.alt)
    height = float(sun.alt) + math.radians(6)
    height /= math.radians(96)
    if height < 0.0:
        height = 0.0
    model.insert_data('sun', height)
except Exception as e:
    log.error(e)
    exit()

