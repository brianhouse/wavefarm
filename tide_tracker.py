#!/usr/bin/env python

import json, model
from housepy import config, log, net

log.info("////////// tide_tracker //////////")

try:
    response = net.read("http://api.wunderground.com/api/%s/rawtide/q/NY/Hudson.json" % config['weather'])
    data = json.loads(response)
    for entry in data['rawtide']['rawTideObs']:
        model.insert_data('tide', entry['height'], t=int(entry['epoch']))
except Exception as e:
    log.error(e)
    exit()

