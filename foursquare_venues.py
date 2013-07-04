#!/usr/bin/env python

import json, model, datetime, math, time
from housepy import config, log, net

log.info("////////// foursquare venues //////////")

# radius in meters
# the limit sucks

anchors = [ "42.3187870,-74.0780210",   # wave farm
            "42.2989749,-73.9984659",   # cairo
            "42.3109186,-74.0554126",   # acra
            "42.2173102,-73.8645734",   # catskill
            "42.2528649,-73.7909590",   # hudson
            "42.3509179,-73.8029028",   # coxsackie
            "42.3095301,-73.7462345",   # stockport
            "42.3292525,-73.6156735",   # ghent
            "42.4134168,-73.6731749",   # valatie
            "42.2603648,-73.8095707",   # athens
            "42.2861974,-73.7387345",   # slottville
            "42.3642516,-73.5948391",   # chatham
            "42.4739705,-73.7923456",   # coeymans
            "42.4684148,-73.8162354",   # ravena
            "42.4461940,-73.7886601",   # new baltimore
            "42.4153596,-74.0220769",   # greeneville
            "42.3995257,-74.1723608",   # durham
            "42.3073065,-74.2520875",   # windham
            "42.2553651,-73.9023518",   # leeds
            "42.1345339,-73.8917982",   # germantown
            "42.2703636,-74.3029229",   # jewett
            "42.2136987,-74.2187541",   # hunter
            "42.1745334,-74.0201355",   # palenville
            "42.0775906,-73.9529126",   # saugerties
            ]


            
total_venues = []

for anchor in anchors:
    params = {'intent': "browse", 'll': anchor, 'radius': 8000, 'limit': 50, 'client_id': config['foursquare']['key'], 'client_secret': config['foursquare']['secret'], 'v': "20130704"}
    params = net.urlencode(params)
    request_string = "https://api.foursquare.com/v2/venues/search?%s" % params
    try:
        response = net.read(request_string)
    except Exception as e:
        log.error(log.exc(e))
        continue
    data = json.loads(response)
    try:
        venues = data['response']['venues']
        for venue in venues:
            checkins = venue['stats']['checkinsCount']
            if checkins == 0:
                continue
            if 'hereNow' in venue:
                people = venue['hereNow']['count']
            else:
                people = 0
            venue_id = venue['id']
            venue = {'venue_id': venue_id, 'people': people}
            log.debug(venue)
            total_venues.append(venue)
    except Exception as e:
        log.error(log.exc(e))
        log.error(json.dumps(data, indent=4))

for venue in total_venues:
    model.add_venue(venue)
log.debug("added %s venues" % len(total_venues))

    