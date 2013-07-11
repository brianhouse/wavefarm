#! /usr/bin/env python

import model, json, time, math
import numpy as np
import signal_processing as sp
from housepy import config, log, util, drawing, science
from housepy.crashdb import CrashDB

# ranges
RANGE = {   'heat': (60, 110),
            'rain': (0, None),
            'wind': (0, 10.0),
            'visibility': (0, 10.0),
            'sun': (0.0, 0.8),
            'tide': (0.0, 5.0),
            'checkins': (0.0, 5.0),
            'checkouts': (0.0, 5.0),
            'tweets': (0.0, 5.0),
            'motion': (0.0, 1.0),
            'sound': (0.0, 1.0),
            'humidity': (70, 100)
        }

DURATION = 3600
# DURATION *= 24

t = int(time.time())
# t = int(time.mktime(util.parse_date('2013-07-10 19:00:00').timetuple()))

filename = "signals/%s_%s.json" % (t, DURATION)
log.info("Generating %s..." % filename)
db = CrashDB(filename)

if config['draw']:
    ctx = drawing.Context(width=2000, height=500, background=(0., 0., 1.), hsv=True, flip=True, relative=True)


def process_readings(kind, color, thickness=5):
    data = model.fetch_readings(kind, t - DURATION, t)
    if not len(data):
        return False
    data.sort(key=lambda d: d['t'])
    ts = [d['t'] for d in data]
    vs = [d['v'] for d in data]
    signal = sp.resample(ts, vs, DURATION)
    signal = sp.normalize(signal, RANGE[kind][0], RANGE[kind][1])
    db[kind] = list(signal)
    if config['draw']:
        ctx.line([(float(i) / DURATION, sample) for (i, sample) in enumerate(signal)], thickness=thickness, stroke=color)

def process_events(kind, color):
    data = model.fetch_events(kind, t - DURATION, t)
    if not len(data):
        return False        
    data.sort(key=lambda d: d['t'])
    events = []
    events = [(d['t'] - (t - DURATION), max(1, round(d['d'])), science.scale(d['v'], RANGE[kind][0], RANGE[kind][1])) for d in data]
    db[kind] = events
    if config['draw']:
        for event in events:        
            ti, d, v = event
            ctx.line(float(ti) / DURATION, v, float(ti + d) / DURATION, v, thickness=10, stroke=color)

process_readings('heat', (0., 1., 1.))   # red
# # process_readings('rain', (.1, 1., 1.))    # orange
# # process_readings('humidity', (.1, 1., 1.))    # orange
process_readings('wind', (.3, 1., 1.))  # green
process_readings('visibility', (.6, 1., 1.))    # blue
process_readings('sun', (0., 0., 0.))    # black
# process_readings('tide', (0., 0., 0.5))    # gray

process_readings('checkins', (.8, .8, 1.))    # purple
process_readings('checkouts', (.9, .8, 1.), 1)    # thin purple

process_events('tweets', (0.55, 1., 1.))    # matrix
# process_events('motion', (0.76, 1., 1.))    # 
process_events('sound', (0.92, 1., 1.))    # crimson

db.close()

log.info("--> ok")

if config['draw']:
    ctx.show()
    filename = "signals/%s_%s.png" % (t, DURATION)
    ctx.image.save(filename, "PNG")

