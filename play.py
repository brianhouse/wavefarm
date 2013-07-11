#!/usr/bin/env python3

import random, sys, urllib.request, json
from housepy import config, log, crashdb
from braid import *
from braid.voice.basic_midi import BasicMidi
from braid.voice.msp_swerve import MspSwerve
from collections import OrderedDict

DURATION = 60
RANGE = 10, 180 # tempo


if len(sys.argv) < 2:
    print("[signal_tag]")
    exit()
signal_tag = sys.argv[1]
if signal_tag == 'live':
    try:
        response = urllib.request.urlopen("http://%s:%s/data" % (config['server']['host'], config['server']['port']))
        data = json.loads(response.read().decode('utf-8'))
        log.info("received %s" % (data.keys(),))
    except Exception as e:
        log.error(log.exc(e))
        exit()
else:
    data = crashdb.CrashDB("signals/%s.json" % signal_tag)
    data.close()

MAP = {#'sun': 'sun',
        'tide': 'sun', 'chin': 'checkins', 'chout': 'checkouts', 'heat': 'heat', 'wind': 'wind', 'visi': 'visibility'}

# a ring of 8 bells
# we are in E major (dom), nice going, guitarist
TUNING = {  #'sun': B1,       # 5
            'tide': E1,     # 1
            'heat': E2,     # 1
            'wind': Ab3,    # 3
            'visi': D3,     # 7
            'chin': A2,     # 4
            'chout': Db3,   # 6
            'tweets': Gb5,  # 2
            'sounds': Gb4,  # 2
            }

sun = BasicMidi(1)

tide = BasicMidi(2)
heat = BasicMidi(3)
wind = BasicMidi(4)
visi = BasicMidi(5)
chin = BasicMidi(7)
chout = BasicMidi(8)
tweets = BasicMidi(9)
sounds = BasicMidi(10)

# 'tide', 'heat', 'wind', 'visi', 'chin', 'chout'

UNIT = 0.75

def intro():
    order = 'tide', 'heat', 'wind', 'visi', 'chin'  # 1- 1, 3, 7, 4
    t = 0.0
    for voice in order:
        def play_intro(voice):
            def intro_callback():
                eval(voice).play(TUNING[voice], 0.8 + (random.random() * 0.2))
            return intro_callback
        driver.callback(play_intro(voice), t)
        t += UNIT
        if voice == 'tide':
            t += UNIT
    t += UNIT * 2
    for voice in ('chin', 'chout', 'visi', 'heat'):     # 6, 3, 7, 1
        def play_intro(voice):
            def intro_callback():
                eval(voice).play(TUNING[voice], 0.8 + (random.random() * 0.2))
            return intro_callback
        driver.callback(play_intro(voice), t)
        t += UNIT
    t += UNIT * 1
    driver.callback(changes, t)


def changes():

    t = 0.0
    for voice in ('tide', 'chin', 'chout', 'heat', 'wind', 'visi'):
        def start_voice(voice):
            def sv():
                eval(voice).tween('tempo', RANGE[0], RANGE[1], DURATION, get_signal_f(data[MAP[voice]]))    # tide->sun
                eval(voice).pattern = TUNING[voice], TUNING[voice]
            return sv
        driver.callback(start_voice(voice), t)
        t += 1.0        


    def play_tweet(v, d):
        def tweet_callback():
            tweets.play(TUNING['tweets'])
        return tweet_callback
    last_t = None
    for tweet in data['tweets']:
        t, v, d = tweet
        t /= 60.0
        # quantize
        t *= 8.0
        t = int(t)
        t /= 8.0
        if last_t is not None and t == last_t:
            continue
        last_t = t      
        t += random.random() * (1.0 / 30)       
        driver.callback(play_tweet(v / 3.0, d), t)
        

    def play_sound(v, d):
        def sound_callback():
            # sounds.play(Gb4, v)
            sounds.play(TUNING['sounds'])
        return sound_callback
    last_t = None
    for sound in data['sound']:
        t, v, d = sound
        t /= 60.0
        # quantize
        t *= 8.0
        t = int(t)
        t /= 8.0
        if last_t is not None and t == last_t:
            continue
        last_t = t      
        t += random.random() * (1.0 / 30)    
        v *= 1.0
        v = min(1.0, v)
        v *= 0.8
        driver.callback(play_sound(v, d), t)

    t = 0.0
    for voice in ('tide', 'chin', 'chout', 'heat', 'wind', 'visi', 'sounds', 'tweets'):
        def soft_stop_voice(voice):
            def sv():
                eval(voice).pattern = 0, 0                
            return sv
        def hard_stop_voice(voice):
            def sv():
                if voice == 'tide':
                    return
                eval(voice).velocity = 0.0
                eval(voice).end()                    
            return sv
        driver.callback(soft_stop_voice(voice), (DURATION - t - 1)) # so we dont get squeltches
        driver.callback(hard_stop_voice(voice), (DURATION - t))
        t += 1.0        

    PAD = 3.0
    def on_finish():
        driver.stop()
    driver.callback(on_finish, DURATION + PAD)


intro()

driver.start()


# I'm doing everything with driver callbacks, but I could have just timed it straight
# but that would be poor form
