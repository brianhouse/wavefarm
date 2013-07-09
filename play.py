#!/usr/bin/env python3

import random, sys
from housepy import config, log, crashdb
from braid import *
from braid.voice.basic_midi import BasicMidi

DURATION = 60

if len(sys.argv) < 2:
	print("[signal_tag]")
	exit()

RANGE = 100, 130

data = crashdb.CrashDB("signals/%s.json" % sys.argv[1])
data.close()

# a ring of 8 bells

TUNING = [None, A2, B2, Db2, D4, E4, Gb4, Ab4, A5]	# typical?
TUNING = [None, B2, E3, Gb3, Ab4, E4, Gb4, Ab4, A5]	# westminster?
TUNING = [None, B2, E3, Gb3, Ab4, D4, Gb4, Ab4, A5]	# alt


sun = BasicMidi(1)
sun.tween('tempo', RANGE[0], RANGE[1], DURATION, get_signal_f(data['sun']))
sun.pattern = TUNING[1], TUNING[1]

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
# rain.tween('tempo', RANGE[0], RANGE[1], DURATION, get_signal_f(data['rain']))
# rain.pattern = TUNING[6], TUNING[6]

# rain = BasicMidi(7)
# rain.tween('tempo', RANGE[0], RANGE[1], DURATION, get_signal_f(data['rain']))
# rain.pattern = TUNING[7], TUNING[7]

# rain = BasicMidi(8)
# rain.tween('tempo', RANGE[0], RANGE[1], DURATION, get_signal_f(data['rain']))
# rain.pattern = TUNING[8], TUNING[8]




# heatbell = BasicMidi(1)
# heatbell.tween('tempo', 80, 120, DURATION, get_signal_f(data['heat']))
# heatbell.chord = B1, MAJ
# heatbell.pattern = 1, 1#[1, 1, 1, 1], [1, 1, 1, 1]

# windbell = BasicMidi(2)
# windbell.tween('tempo', 80, 120, DURATION, get_signal_f(data['wind']))
# windbell.chord = E2, MAJ
# windbell.pattern = 1, 1#[1, 1, 1, 1], [1, 1, 1, 1]


# windbell = BasicMidi(3)
# windbell.tween('tempo', 120, 200, DURATION, get_signal_f(data['wind']))
# windbell.chord = Gb2, MAJ
# windbell.pattern = 1, 1#[1, 1, 1, 1], [1, 1, 1, 1]


# def on_finish():
#     driver.stop()
# driver.callback(on_finish, DURATION)


driver.start()


