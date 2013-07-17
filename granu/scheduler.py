#!/usr/bin/env python

import time, process, subprocess, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from housepy import config, log, s3, osc

log.info("Starting recording...")
filename = "%s.wav" % int(time.time())
record_sender = osc.Sender(5280)
record_sender.send('/record', filename)

log.info("Triggering playback...")
subprocess.call("/usr/local/bin/python3 play.py live", shell=True)

DURATION = 75
time.sleep(DURATION)

log.info("Uploading...")

if s3.upload(filename):
    log.info("Removing file...")
    os.remove(filename)