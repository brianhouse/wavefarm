#!/usr/bin/env python

import os, sys, json, model
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from housepy import config, log, tornado_server, process

log.info("////////// server //////////")

process.secure_pid(os.path.join(os.path.dirname(__file__), "run"))


class Home(tornado_server.Handler):

    def get(self, page=None):
        log.info("Home")
        return self.text("Hello there!")

    def post(self, nop=None):
        log.info("Home.post")
        try:
            data = json.loads(self.request.body)
            for entry in data:
                if 'duration' in entry:
                    log.info("%s,%s (e): %s%s" % (entry['device'], entry['kind'], entry['value'], (" %s" % entry['quality'] if 'quality' in entry else "")))
                    model.insert_event(entry['device'], entry['kind'], entry['value'], entry['t'], entry['duration'], entry['quality'] if 'quality' in entry else None)                                    
                else:
                    log.info("%s,%s (r): %s" % (entry['device'], entry['kind'], entry['value']))
                    model.insert_reading(entry['device'], entry['kind'], entry['value'], entry['t'])                                        
        except Exception as e:
            return self.error(log.exc(e))
        return self.text("OK")


def main():
    handlers = [
        (r"/?([^/]*)", Home),
    ]
    tornado_server.start(handlers)      
                    

if __name__ == "__main__":
    main()

