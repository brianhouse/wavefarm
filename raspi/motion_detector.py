#!/usr/bin/env python

import sys, cv, time, os, numpy, random, threading, Queue
from collections import deque        
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from housepy import log, config, util, net


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
            while time.time() - start_t <= 5:#1 * 60:
                time.sleep(0.1)
            log.info("Reporting...")
            values = []
            while True:
                try:
                    value = self.queue.get_nowait()
                    values.append(value)
                except Queue.Empty:
                    break
            motion = sum(values) / float(len(values))
            log.info("--> motion: %s" % motion)
            response = net.read("http://%s:%s" % (config['server']['host'], config['server']['port']), {'name': config['name'], 'source': "motion", 'value': motion, 't': time.time()})
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
    # print(level)
    reporter.queue.put(level)

    if config['show_video']:
        cv.ShowImage("motion", mat_result)
    cv.WaitKey(5)

