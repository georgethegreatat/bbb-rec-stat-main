#!/bin/bash

echo Cloning repository...
git pull
echo Updating script
sudo rm /home/s2.py
sudo cp /home/bbb-rec-stat-main/Back/s2.py /home/s2.py
echo Done.
echo Testing script...
python3 /home/s2.py
echo Script working! Have a nice day.
echo Please do not forget about adding cron-job for sript. More info: https://github.com/georgethegreatat/bbb-rec-stat-main