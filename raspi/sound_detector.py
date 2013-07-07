#! /usr/bin/env python

import os, sys, wave, time, json, math
import numpy as np
from housepy import log, config, util, science, drawing, jobs
from scipy.io import wavfile

THRESHOLD = 0.05 # as percentage of maximum gain

def handle_audio(data):

    filename = data['filename']
    t = data['t']

    sample_rate, signal = wavfile.read("tmp/" + filename)
    log.info("AUDIO SAMPLES %s" % len(signal))
    log.info("SAMPLE RATE %s" % sample_rate)
    duration = float(len(signal)) / sample_rate
    log.info("AUDIO DURATION %ss" % util.format_time(duration))
    signal = (np.array(signal).astype('float') / (2**16 * 0.5))   # assuming 16-bit PCM, -1 - 1

    magnitude = abs(signal)

    thresholded_magnitude = (magnitude > THRESHOLD) * magnitude
    # level = science.smooth(thresholded_magnitude, window_len=1000)
    average_magnitude = np.average(thresholded_magnitude)
    log.info("AVERAGE MAGNITUDE %s" % average_magnitude)

    os.remove("tmp/" + filename)


    # # show magnitude processing -- use to determine noise floor
    # ctx = drawing.Context(width=800, height=300, background=(0., 0., 1.), hsv=True, flip=True, relative=True)
    # ctx.line([(float(i) / len(magnitude), sample) for (i, sample) in enumerate(magnitude)], thickness=1, stroke=(0., 0., 0.5))
    # ctx.line([(float(i) / len(thresholded_magnitude), sample) for (i, sample) in enumerate(thresholded_magnitude)], thickness=1, stroke=(0., 0., 0.))
    # # ctx.line([(float(i) / len(level), sample) for (i, sample) in enumerate(level)], thickness=1, stroke=(0., 1., 1.))
    # ctx.line(0.0, THRESHOLD, 1.0, THRESHOLD, thickness=1, stroke=(0.55, 1., 1.))
    # ctx.show()



    # more fun:

    # # show time domain
    # ctx = drawing.Context(width=800, height=300, background=(0., 0., 1.), hsv=True, flip=True, relative=True)
    # ctx.line([(float(i) / len(signal), (sample * 0.5) + 0.5) for (i, sample) in enumerate(signal)], thickness=1)
    # ctx.show()

    # # frequency domain
    # # http://xoomer.virgilio.it/sam_psy/psych/sound_proc/sound_proc_python.html
    # # http://www.mathworks.com/support/tech-notes/1700/1702.html
    # fsig = np.fft.fft(signal)
    # n = len(fsig)
    # unique_pts = math.ceil((n + 1) / 2.0)           # fft is symmetric, throw away second half
    # fsig = fsig[0:unique_pts]   
    # fsig = abs(fsig)                                # get the magnitude of the signal
    # fsig /= float(n)                                # scale it by the length of the original signal
    # fsig **= 2                                      # square it to get the power
    # if n % 2 == 0:                                  # multiply by two to keep the same energy, since we dropped half the signal (but dont multiply the nyquist, if it exists)
    #     fsig[1:len(fsig) - 1] *= 2
    # else:
    #     fsig[1:len(fsig)] *= 2
    # display_fsig = [10 * np.log10(sample) for sample in fsig]
    # display_fsig = science.normalize(display_fsig)
    # ctx = drawing.Context(width=800, height=300, background=(0., 0., 1.), hsv=True, flip=True, relative=True)
    # ctx.line([(float(i) / len(display_fsig), sample) for (i, sample) in enumerate(display_fsig)], thickness=1)
    # ctx.show()

    log.info("//////////")
    

queue = jobs.Jobs()
queue.process(handle_audio, tube="audio")


