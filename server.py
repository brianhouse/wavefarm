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
            device = self.get_argument("device")
            kind = self.get_argument("kind")
            value = float(self.get_argument("value"))
            t = self.get_argument("t", None)
            if t is None:
                start_t = self.get_argument("start_t")
                stop_t = self.get_argument("stop_t")
                quality = self.get_argument("quality")
                log.info("%s, %s (e): %s-%s" % (device, kind, value, quality))
                model.insert_event(device, kind, value, t)                
            else:
                log.info("%s, %s (r): %s" % (device, kind, value))
                model.insert_reading(device, kind, value, t)
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

