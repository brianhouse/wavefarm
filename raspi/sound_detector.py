#! /usr/bin/env python

import os, sys, time, json, math, threading, subprocess, Queue, gc
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import signal_processing as sp
import numpy as np
from housepy import log, config, util, net
from scipy.io import wavfile

THRESHOLD = 0.025 # as percentage of maximum gain

class Recorder(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.queue = Queue.Queue()
        self.start() 

    def run(self):
        while True:
            t = int(time.time())
            try:
                command = "arecord -D plughw:1,0 -d 30 -f S16_LE -c1 -r44100 -t wav audio_tmp/%s.wav" % t
                log.info("%s" % command)
                subprocess.check_call(command, shell=True)    # 30s of cd-quality audio  
            except Exception as e:
                log.error(log.exc(e))
                time.sleep(1)
                continue
            log.info("--> ok")
            self.queue.put(t)


def process(t):

    log.info("////////// process %s //////////" % t)
    filename = "audio_tmp/%s.wav" % t
    sample_rate, signal = wavfile.read(filename)
    log.info("AUDIO SAMPLES %s" % len(signal))
    log.info("SAMPLE RATE %s" % sample_rate)
    duration = float(len(signal)) / sample_rate
    log.info("AUDIO DURATION %ss" % util.format_time(duration))
    signal = (np.array(signal).astype('float') / (2**16 * 0.5))   # assuming 16-bit PCM, -1 - 1

    log.info("--> preprocessing")
    magnitude = abs(signal)
    thresholded_magnitude = (magnitude > THRESHOLD) * magnitude
    # level = sp.smooth(thresholded_magnitude, size=10000)      # shit -- smooth is too expensive for raspi
    level = thresholded_magnitude

    log.info("--> scanning")
    TOLERANCE = sample_rate / 10    # within a tenth of a second, same sound (poor man's smoothing?)
    indexes = []
    maxes = []
    durations = []
    zeros = 0
    on_chunk = False
    for index, sample in enumerate(level):
        if sample > 0.0:
            if not on_chunk:
                indexes.append(index)                
                durations.append(0)
                maxes.append(0)
                on_chunk = True              
            durations[-1] += 1
            if sample > maxes[-1]:
                maxes[-1] = sample
            zeros = 0            
        if sample == 0.0:            
            if on_chunk:
                zeros += 1
                if zeros == TOLERANCE:
                    on_chunk = False
    events = []
    for i in xrange(len(indexes)):
        value, t_, duration = maxes[i], t + int(float(indexes[i]) / sample_rate), float(durations[i]) / sample_rate
        events.append((value, t_, duration))
    for event in events:
        log.debug(event)

    if 'draw' in config and config['draw']:   
        from housepy import drawing    
        log.info("--> drawing")
        ctx = drawing.Context(width=2000, height=500, background=(0., 0., 1.), hsv=True, flip=True, relative=True)
        ctx.line([(float(i) / len(magnitude), sample) for (i, sample) in enumerate(magnitude)], thickness=1, stroke=(0., 0., 0.5))
        ctx.line([(float(i) / len(thresholded_magnitude), sample) for (i, sample) in enumerate(thresholded_magnitude)], thickness=1, stroke=(0., 0., 0.))
        ctx.line([(float(i) / len(level), sample) for (i, sample) in enumerate(level)], thickness=1, stroke=(0., 1., 1.))
        level = sp.normalize(level)
        ctx.line([(float(i) / len(level), sample) for (i, sample) in enumerate(level)], thickness=1, stroke=(0.15, 1., 1.))
        ctx.line(0.0, THRESHOLD, 1.0, THRESHOLD, thickness=1, stroke=(0.55, 1., 1.))
        ctx.show()

    try:
        data = []
        for event in events:
            value, t_, duration = event
            data.append({'device': config['device'], 'kind': "sound", 'value': value, 't': t_, 'duration': duration})
        response = net.read("http://%s:%s" % (config['server']['host'], config['server']['port']), json.dumps(data))
        log.info(response)
    except Exception as e:
        log.error(log.exc(e))

    if config['device'] != "Granu":
        os.remove(filename)


if len(sys.argv) > 1:
    t = sys.argv[1]
    process(int(t))
else:    
    recorder = Recorder()
    while True:
        t = recorder.queue.get()
        try:
            process(t)
        except Exception as e:
            log.error(log.exc(e))
        time.sleep(0.01)


# http://stackoverflow.com/questions/2473783/is-there-a-way-to-circumvent-python-list-append-becoming-progressively-slower