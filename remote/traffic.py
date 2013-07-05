#!/usr/bin/env python

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import json, model
from housepy import config, log, net
from PIL import Image

log.info("////////// traffic //////////")

lon, lat = -74.0780210, 42.3187870 

# try:
source = "http://www.mapquestapi.com/traffic/v2/flow?key=%s&mapLat=%s&mapLng=%s&mapHeight=400&mapWidth=400&mapScale=433343" % (config['mapquest'], lat, lon)
log.debug(source)
response = net.grab(source, "traffic.gif")

image = Image.open("traffic.gif")
print(image.info)
print(dir(image))
image.show()


# except Exception as e:
#     log.error(log.exc(e))
#     exit()

