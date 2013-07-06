#!/usr/bin/env python

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import json, model, datetime, math
from housepy import config, log, net

log.info("////////// foursquare //////////")

update = []
checkins = 0
checkouts = 0

for venue in model.get_venues():
    log.debug("checking %s" % venue['venue_id'])
    try:
        params = {'client_id': config['foursquare']['key'], 'client_secret': config['foursquare']['secret'], 'v': "20130704"}
        params = net.urlencode(params)
        request_string = "https://api.foursquare.com/v2/venues/%s/herenow?%s" % (venue['venue_id'], params)
        response = net.read(request_string, timeout=1)
        data = json.loads(response)
        people = data['response']['hereNow']['count']
        if people != venue['people']:
            if people > venue['people']:
                checkins += people - venue['people']
            else:
                checkouts += venue['people'] - people
            venue['people'] = people
            update.append(venue)
    except Exception as e:
        log.error(log.exc(e))

# print(json.dumps(update, indent=4))
model.update_venues(update)

model.insert_data('checkins', checkins)
model.insert_data('checkouts', checkouts)



