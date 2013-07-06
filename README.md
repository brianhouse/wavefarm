wavefarm
========

resolution is 5 mins

Install, OS X
-------------
ps3eye for mountain lion, macam: http://forum.openframeworks.cc/index.php?topic=12021.0

    brew install pyportaudio
    sudo pip install pyaudio

Install, RasPI
--------------
    sudo apt-get update
    sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
    sudo easy_install pip

    sudo pip install pyaudio
    


Server reminders
----------------
    cp wavefarm/ngnix.conf /etc/nginx/
    sudo service nginx start

    sudo ntpdate time.nist.gov  # in sudo crontab


### Copyright/License

Copyright (c) 2013 Brian House

This program is free software licensed under the GNU General Public License, and you are welcome to redistribute it under certain conditions. It comes without any warranty whatsoever. See the LICENSE file for details, or see <http://www.gnu.org/licenses/> if it is missing.

Projects that use this software must credit Brian House and link to http://brianhouse.net
