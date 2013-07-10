#!/usr/bin/env python3

import random, sys
from housepy import config, log, crashdb
from braid import *
from braid.voice.basic_midi import BasicMidi
from braid.voice.msp_swerve import MspSwerve

DURATION = 60

if len(sys.argv) < 2:
    print("[signal_tag]")
    exit()

RANGE = 60, 120

data = crashdb.CrashDB("signals/%s.json" % sys.argv[1])
data.close()

# a ring of 8 bells
# we are in E major, nice going, guitarist

TUNING = [None, A2, B2, Db2, D4, E4, Gb4, Ab4, A5]  # typical?
TUNING = [None, B2, E3, Gb3, Ab4, E4, Gb4, Ab4, A5] # westminster?
TUNING = [None, B2, E3, Gb3, Ab4, D3, Gb4, Ab4, A5] # alt, octaves off
TUNING = [None, B1, E1, Gb2, Ab3, D3, None, A2, Db3]    # alt
TUNING = [None, B1, E1, E2, Ab3, D3, Gb3, A2, Db3]  # alt  # 5 1 1 3 7 2 4 6



sun = MspSwerve(1)
sun.synth = 'cycle'
sun.attack = 800
sun.sustain = 300
sun.release = 4100
sun.reverb = 0.7, 0.3, 1., 0.2, 0.5
sun.tween('tempo', RANGE[0] * 0.5, RANGE[1] * 0.5, DURATION, get_signal_f(data['sun']))
sun.pattern = TUNING[1], TUNING[1]

#

tide = BasicMidi(2)
tide.tween('tempo', RANGE[0], RANGE[1], DURATION, get_signal_f(data['tide']))
tide.pattern = TUNING[2], TUNING[2]

heat = BasicMidi(3)
heat.tween('tempo', RANGE[0], RANGE[1], DURATION, get_signal_f(data['heat']))
heat.pattern = TUNING[3], TUNING[3]

wind = BasicMidi(4)
wind.tween('tempo', RANGE[0], RANGE[1], DURATION, get_signal_f(data['wind']))
wind.pattern = TUNING[4], TUNING[4]

visi = BasicMidi(5)
visi.tween('tempo', RANGE[0], RANGE[1], DURATION, get_signal_f(data['visibility']))
visi.pattern = TUNING[5], TUNING[5]

# rain = BasicMidi(6)
# rain.tween('tempo', RANGE[0], RANGE[1], DURATION, get_signal_f(data['humidity']))
# rain.pattern = TUNING[6], TUNING[6]

chin = BasicMidi(7)
chin.tween('tempo', RANGE[0], RANGE[1], DURATION, get_signal_f(data['checkins']))
chin.pattern = TUNING[7], TUNING[7]

chout = BasicMidi(8)
chout.tween('tempo', RANGE[0], RANGE[1], DURATION, get_signal_f(data['checkouts']))
chout.pattern = TUNING[8], TUNING[8]



# tweets = MspSwerve(9)
# tweets.synth = 'wave'
# tweets.chord = C8, MAJ
# tweets.attack = 0
# tweets.sustain = 0
# tweets.release = 1
# tweets.reverb = 0.7, 0.3, 0.2, .9, 0.1
# tweets.fade = 0.0
# tweets.velocity = 1.0

tweets = BasicMidi(9)
def play_tweet(v, d):
    def tweet_callback():
        tweets.play(A5, v)
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
    

# sounds = MspSwerve(10)

# sounds.synth = 'saw'
# sounds.attack = 5
# sounds.sustain = 10
# sounds.release = 25
# sounds.reverb = 0.8, 0.2, 0.5, 0.0, 0.0

# sounds.synth = 'noise'
# sounds.attack = 5
# sounds.sustain = 0
# sounds.release = 30
# sounds.reverb = 0.2, 0.8, 0.8, 0.0, 0.5

# sounds.fade = 0.0


sounds = BasicMidi(10)
def play_sound(v, d):
    def sound_callback():
        # sounds.play(Gb4, v)
        sounds.play(Gb5, v)
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


def on_finish():
    driver.stop()
driver.callback(on_finish, DURATION)


driver.start()


