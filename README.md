Wavefarm
========

resolution is 5 mins



Server
======

    cp wavefarm/ngnix.conf /etc/nginx/
    sudo service nginx start

    sudo ntpdate time.nist.gov  # in sudo crontab, daily


Raspi
======

    sudo apt-get install libcv-dev
    sudo apt-get install python-opencv

    sudo nano /etc/network/interfaces

cron:

    */5 * * * * ping -c4 'google.com' > /dev/null; if [ $? != 0 ]; then ifdown --force wlan0; ifup wlan0; fi


audio:

    arecord -l                                  # list devices
    arecord -d 10 -f cd -t wav foobar.wav       # record




### Copyright/License

Copyright (c) 2013 Brian House

This program is free software licensed under the GNU General Public License, and you are welcome to redistribute it under certain conditions. It comes without any warranty whatsoever. See the LICENSE file for details, or see <http://www.gnu.org/licenses/> if it is missing.

Projects that use this software must credit Brian House and link to http://brianhouse.net
