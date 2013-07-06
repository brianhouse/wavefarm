#!/usr/bin/env python

import sys, cv, time, os, numpy, random 
from collections import deque        
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from housepy import log, config, util

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
    print(level)

    if config['show_video']:
        cv.ShowImage("motion", mat_result)

