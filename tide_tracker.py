#!/usr/bin/env python

import json, model
from housepy import config, log, net

log.info("////////// tide_tracker //////////")

"""
This pulls the next five days or so, and timestamps in 5 minutes increments starting from querytime.
So always run it on the hour to avoid weird resolution, and dont have to run it very often.

"""

try:
    response = net.read("http://api.wunderground.com/api/%s/rawtide/q/NY/Hudson.json" % config['weather'])
    data = json.loads(response)
    for entry in data['rawtide']['rawTideObs']:
        model.insert_data('tide', entry['height'], t=int(entry['epoch']))
except Exception as e:
    log.error(e)
    exit()

