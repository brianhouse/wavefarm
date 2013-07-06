#! /usr/bin/env python

import sys, wave, pyaudio, time, json
from housepy import log, config
# from housepy import jobs

DURATION = 60
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1    # changing this will break things
RATE = 44100
DEVICE_NAME = "USB Camera-B4.09.24.1"
# DEVICE_NAME = "Built-in Microph"


# jobs.launch_beanstalkd()
# queue = jobs.Jobs()

device = None
def record():
    global device    
    audio = pyaudio.PyAudio()    
    if device is None:
        for d in xrange(audio.get_device_count()):
            info = audio.get_device_info_by_index(d)
            log.info(json.dumps(info, indent=4))
            if DEVICE_NAME in info['name']:
                device = d
                log.info("Found device")
        if device is None:
            log.info("Device not found!")
            exit()        
    log.info("Recording...")
    t = time.time()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE, input_device_index=device)
    chunks = []
    for i in xrange((RATE / CHUNK_SIZE) * DURATION):
        try:
            chunk = stream.read(CHUNK_SIZE)
            chunks.append(chunk)
        except Exception as e:
            log.error(log.exc(e))
    binary_data = ''.join(chunks)    
    stream.close()
    audio.terminate()
    log.info("--> done")

    filename = str(int(t)) + ".wav"
    log.info("Writing file %s..." % filename)
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(binary_data)
    wf.close()
    log.info("--> done")

    # queue.add(tube='audio', data={'filename': filename, 't': t})

    log.info("//////////")


while True:
    record()
