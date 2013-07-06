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
            name = self.get_argument("name")
            source = self.get_argument("source")
            events = self.get_argument("events")
            events = json.loads(events)        
            log.info("%s: %s (%s)" % (name, events, source))
            return self.text("OK")
        except Exception as e:
            return self.error(log.exc(e))


def main():
    handlers = [
        (r"/?([^/]*)", Home),
    ]
    tornado_server.start(handlers)      
                    

if __name__ == "__main__":
    main()

