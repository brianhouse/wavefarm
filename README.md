Wavefarm
========

Strategy
--------

scale is 60:1
one minute becomes one second, etc.
one second becomes 60hz, which is about musical time. (16ths at 120bpm is 32hz)

--

two types of data: continuous measurements, and discrete events, reflected in the model

'readings' just have a value. if the value repeats, we will assume it's constant. intended to be resampled.
readings are taken every 5 minutes (-> 5 seconds)

with 'events', value is intensity. they also have a duration, and optionally a quality.
events are quantized to every second (32nd note)

see crontab.smp for a list of sources and types


Discussion
----------

What is the nature of remote monitoring? What can we know and not know through data?

Rhythamanlysis vs surveillance

Alternative relationship to data


Checklist
---------
server is running
MainStage loaded and set to soundflower
MaxMSP loaded and set to soundflower

wow upload at wavefarm is so slow



Setup
=====

Requires housepy and signal_processing and braid

Server
------

    sudo cp wavefarm/ngnix.conf /etc/nginx/
    sudo service nginx restart

    tzselect
    echo "America/New_York" | sudo tee /etc/timezone
    sudo dpkg-reconfigure --frontend noninteractive tzdata
    sudo ntpdate time.nist.gov  # in sudo crontab, daily

    sudo pip install tweepy
    sudo pip install pyephem


Raspis
------

    ssh 10.0.1.45 -l pi
    ssh 10.0.1.169 -l pi

    sudo nano /etc/network/interfaces

    sudo apt-get update
    sudo apt-get install libcv-dev
    sudo apt-get install python-opencv
    sudo apt-get install python-scipy
    sudo apt-get install mercurial

    sudo easy_install pip
    sudo pip install PyYAML

cron:

    */5 * * * * ping -c4 'google.com' > /dev/null; if [ $? != 0 ]; then ifdown --force wlan0; ifup wlan0; fi


audio:

    arecord -l                                                # list devices
    arecord -D plughw:1,0 -d 10 -f S16_LE -c1 -r44100 -t wav foobar.wav       # record (CD-quality but mono, otherwise "-f cd" shortcut)




### Copyright/License

Copyright (c) 2013 Brian House

This program is free software licensed under the GNU General Public License, and you are welcome to redistribute it under certain conditions. It comes without any warranty whatsoever. See the LICENSE file for details, or see <http://www.gnu.org/licenses/> if it is missing.

Projects that use this software must credit Brian House and link to http://brianhouse.net
