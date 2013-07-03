#!/usr/bin/env python

import json, model
from housepy import config, log, net

log.info("////////// weather_station //////////")

try:
    response = net.read("http://api.wunderground.com/api/%s/conditions/q/NY/Acra.json" % config['weather'])
    data = json.loads(response)
    model.insert_data('heat', float(data['current_observation']['heat_index_f']))
    model.insert_data('rain', float(data['current_observation']['precip_today_in']), True)
    model.insert_data('wind', float(data['current_observation']['wind_mph']) / float(data['current_observation']['wind_gust_mph']))
    model.insert_data('visibility', float(data['current_observation']['visibility_mi']))
except Exception as e:
    log.error(e)
    exit()



"""
{
    "current_observation": {
        "heat_index_c": 31, 
        "local_tz_long": "America/New_York", 
        "observation_location": {
            "city": "Freehold", 
            "full": "Freehold, New York", 
            "elevation": "587 ft", 
            "country": "US", 
            "longitude": "-74.039482", 
            "state": "New York", 
            "country_iso3166": "US", 
            "latitude": "42.362419"
        }, 
        "weather": "Mostly Cloudy", 
        "local_time_rfc822": "Wed, 03 Jul 2013 13:11:41 -0400", 
        "forecast_url": "http://www.wunderground.com/US/NY/Acra.html", 
        "windchill_c": "NA", 
        "estimated": {}, 
        "windchill_f": "NA", 
        "pressure_in": "30.17", 
        "dewpoint_string": "75 F (24 C)", 
        "solarradiation": "", 
        "ob_url": "http://www.wunderground.com/cgi-bin/findweather/getForecast?query=42.362419,-74.039482", 
        "local_epoch": "1372871501", 
        "icon_url": "http://icons-ak.wxug.com/i/c/k/mostlycloudy.gif", 
        "display_location": {
            "city": "Acra", 
            "full": "Acra, NY", 
            "magic": "1", 
            "state_name": "New York", 
            "zip": "12405", 
            "country": "US", 
            "longitude": "-74.05583191", 
            "state": "NY", 
            "wmo": "99999", 
            "country_iso3166": "US", 
            "latitude": "42.31083298", 
            "elevation": "203.00000000"
        }, 
        "precip_today_string": "0.02 in (1 mm)", 
        "dewpoint_f": 75, 
        "dewpoint_c": 24, 
        "precip_today_metric": "1", 
        "feelslike_c": "27.6", 
        "image": {
            "url": "http://icons-ak.wxug.com/graphics/wu2/logo_130x80.png", 
            "link": "http://www.wunderground.com", 
            "title": "Weather Underground"
        }, 
        "wind_mph": 0.0, 
        "wind_gust_kph": "11.3", 
        "feelslike_f": "88", 
        "local_tz_short": "EDT", 
        "precip_today_in": "0.02", 
        "heat_index_f": 88, 
        "temp_f": 81.7, 
        "station_id": "KNYFREEH2", 
        "windchill_string": "NA", 
        "temp_c": 27.6, 
        "visibility_km": "16.1", 
        "pressure_trend": "-", 
        "visibility_mi": "10.0", 
        "wind_string": "Calm", 
        "pressure_mb": "1022", 
        "temperature_string": "81.7 F (27.6 C)", 
        "wind_dir": "South", 
        "icon": "mostlycloudy", 
        "wind_degrees": 188, 
        "precip_1hr_in": "0.00", 
        "local_tz_offset": "-0400", 
        "wind_kph": 0.0, 
        "wind_gust_mph": "7.0", 
        "observation_time": "Last Updated on July 3, 1:11 PM EDT", 
        "UV": "6", 
        "heat_index_string": "88 F (31 C)", 
        "observation_epoch": "1372871471", 
        "precip_1hr_metric": " 0", 
        "relative_humidity": "80%", 
        "observation_time_rfc822": "Wed, 03 Jul 2013 13:11:11 -0400", 
        "precip_1hr_string": "0.00 in ( 0 mm)", 
        "feelslike_string": "88 F (27.6 C)", 
        "history_url": "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=KNYFREEH2"
    }, 
    "response": {
        "termsofService": "http://www.wunderground.com/weather/api/d/terms.html", 
        "version": "0.1", 
        "features": {
            "conditions": 1
        }
    }
}
"""