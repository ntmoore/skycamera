#!/bin/bash
# make sure the time is current
/etc/init.d/ntp stop
until ping -nq -c3 8.8.8.8; do
   echo "Waiting for network..."
done
ntpdate -s time.nist.gov
/etc/init.d/ntp start

date >> /home/pi/skyphotos/reboot_times.txt
cd /home/pi/skyphotos/data
python /home/pi/skyphotos/bin/take_day_and_night_pictures.py >> /home/pi/skyphotos/skyphotos.log
