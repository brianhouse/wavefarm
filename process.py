#! /usr/bin/env python

import model, json, time
import numpy as np
import signal_processing as sp
from housepy import config, log, util, drawing

# ranges
RANGE = {   'heat': (60, 110),
            'rain': (0, None),
            'wind': (0, 10.0),
            'visibility': (0, 10.0),
            'sun': (0.0, 1.0),
            'tide': (0.0, 6.0)
        }

DURATION = 3600
DURATION *= 24

t = int(time.time())
t = time.mktime(util.parse_date('2013-07-08 12:00:00').timetuple())

ctx = drawing.Context(width=2000, height=500, background=(0., 0., 1.), hsv=True, flip=True, relative=True)


def process_reading(kind, color):
    data = model.fetch_readings(kind, t - DURATION, t)
    if not len(data):
        return False
    data.sort(key=lambda d: d['t'])
    ts = [d['t'] for d in data]
    vs = [d['v'] for d in data]
    signal = sp.resample(ts, vs, DURATION)
    signal = sp.normalize(signal, RANGE[kind][0], RANGE[kind][1])

    ctx.line([(float(i) / DURATION, sample) for (i, sample) in enumerate(signal)], thickness=5, stroke=color)


process_reading('heat', (0., 1., 1.))   # red
process_reading('rain', (0.1, 1., 1.))    # orange
process_reading('wind', (0.3, 1., 1.))  # green
process_reading('visibility', (0.6, 1., 1.))    # blue
process_reading('sun', (0., 0., 0.))    # black
process_reading('tide', (0., 0., 0.5))    # gray


ctx.show()

