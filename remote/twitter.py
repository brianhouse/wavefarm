#!/usr/bin/env python

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import json, model, datetime, math, tweepy, threading, Queue, time
from housepy import config, log, net, process

log.info("////////// twitter //////////")

process.secure_pid(os.path.join(os.path.dirname(__file__), "..", "run"))

class TweetListener(tweepy.streaming.StreamListener):

    def __init__(self, queue):
        self.queue = queue

    def on_data(self, data):
        tweet = json.loads(data)
        log.debug("@%s: %s" % (tweet['user']['screen_name'], tweet['text']))
        # log.debug(json.dumps(data, indent=4))
        self.queue.put(1)
        return True

    def on_error(self, status):
        log.error(status)


class TweetThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.queue = Queue.Queue()
        self.start()   

    def run(self):     
        tweet_listener = TweetListener(self.queue)
        auth = tweepy.OAuthHandler(config['twitter']['consumer_key'], config['twitter']['consumer_secret'])
        auth.set_access_token(config['twitter']['access_token'], config['twitter']['access_token_secret'])
        stream = tweepy.Stream(auth, tweet_listener)
        stream.filter(locations=[-74.333496,42.034441,-73.432617,42.597008])


tweet_thread = TweetThread()
while True:
    count = 0
    start_t = time.time()
    while time.time() - start_t <= 1.0:
        try:
            tweet = tweet_thread.queue.get_nowait()
            count += 1
        except Queue.Empty:
            pass   
        time.sleep(0.2)
    model.insert_data('tweets', count)                

