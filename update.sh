#!/bin/bash

cd /home/bbb-rec-stat-main/
echo Cloning repository...
git pull
echo Updating script
sudo rm /home/s2.py
sudo mv /home/bbb-rec-stat-main/s2.py /home/s2.py
echo Done.
echo Please do not forget about adding cron-job for sript. More info: https://github.com/georgethegreatat/bbb-rec-stat-main