#!/usr/bin/env python

import sys, cv, time, os, numpy, random 
from collections import deque        
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from housepy import log, config, util

cv.NamedWindow("cam", cv.CV_WINDOW_AUTOSIZE)
capture = cv.CaptureFromCAM(0)

def repeat():

    frame = cv.QueryFrame(capture)
    cv.ShowImage("w1", frame)


while True:
    repeat()