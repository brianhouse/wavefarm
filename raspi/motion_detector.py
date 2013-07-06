#!/usr/bin/env python

import sys, cv, time, os, numpy, random, threading, Queue, json
from collections import deque        
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from housepy import log, config, util, net


# throttles event reporting to every minute
class Reporter(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.queue = Queue.Queue()
        self.start() 

    def run(self):
        while True:
            log.info("Waiting...")
            start_t = time.time()
            while time.time() - start_t <= 60:
                time.sleep(0.2)
            log.info("Reporting...")
            events = []
            while True:
                try:
                    event = self.queue.get_nowait()
                    events.append(event)
                except Queue.Empty:
                    break
            response = net.read("http://%s:%s" % (config['server']['host'], config['server']['port']), {'name': config['name'], 'source': "motion", 'events': json.dumps(events)})
            log.info(response)


reporter = Reporter()

if config['show_video']:
    cv.NamedWindow("cam", cv.CV_WINDOW_AUTOSIZE)
capture = cv.CaptureFromCAM(0)

frame = cv.QueryFrame(capture)
mat_one = cv.CreateMat(frame.height, frame.width, cv.CV_8U)
mat_two = cv.CreateMat(frame.height, frame.width, cv.CV_8U)
mat_result = cv.CreateMat(frame.height, frame.width, cv.CV_8U)
cv.CvtColor(frame, mat_two, cv.CV_RGB2GRAY)    

event_started = False

while True:

    frame = cv.QueryFrame(capture)
    cv.CvtColor(frame, mat_one, cv.CV_RGB2GRAY)    
    cv.AbsDiff(mat_one, mat_two, mat_result)    
    cv.Copy(mat_one, mat_two)    

    cv.Smooth(mat_result, mat_result, cv.CV_BLUR, 5, 5)
    cv.MorphologyEx(mat_result, mat_result, None, None, cv.CV_MOP_OPEN)
    cv.MorphologyEx(mat_result, mat_result, None, None, cv.CV_MOP_CLOSE)
    cv.Threshold(mat_result, mat_result, 10, 255, cv.CV_THRESH_BINARY)

    level = float(cv.CountNonZero(mat_result)) / (frame.height * frame.width)
    if level > config['motion_threshold']:
        if not event_started:
            log.info("starting event!")
            event_started = True
            levels = []
            zeros = config['motion_forgiveness']
            start_t = time.time()
        levels.append(level)
    if level < config['motion_threshold'] or time.time() - start_t >= 30.0:   # force end after 30 seconds
        if event_started:
            if zeros == 0:
                log.info("event ended!")              
                stop_t = time.time() 
                motion = sum(levels) / float(len(levels))
                event = start_t, stop_t, motion
                log.info("--> %s" % motion)
                reporter.queue.put(event)                
                event_started = False
                levels = []     
                zeros = config['motion_forgiveness']       
            else:
                zeros -= 1

    if config['show_video']:
        cv.ShowImage("motion", mat_result)
    cv.WaitKey(5)


