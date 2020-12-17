BBBRSS - BigBlueButton Recordings Statistic Script.

This script giving you Meetings Stat (if it was recorded) on Web-page with minimal UI. 
For now you able to find there:
- General meeting information (start/end time, conf.name, partisipants nubmer etc)
- User lists with LogIN, LogOut time and Standing time in conference
- Download .cvs feature - download button for download user list with all additional information in CSV format for integrate with crm or another service
- Download .html feature - download button for download user list in html-table
- Download .mp4 feature [Development stage] - for now you can download the record if it was converted to mp4 format by jibon57's bbb-recorder script. Soon you will be able to choose what exactly conference start to convert and download.
- Watch your conference record onlite at meeting info-page


**Deployment for one server (not cluster):

1. cd /home
2. git clone https://github.com/georgethegreatat/bbb-rec-stat-main/
3. cd bbb-rec-stat-main/
5. chmod a+x update.sh
6. ./update.sh
7. Put into crontab (if you're not 'vi' fun you can use 'EDITOR=nano crontab -e' command):
> 00 09-21 * * * python3 /home/s2.py >> /var/log/bbb-stat.log # this command running script every 60 min
8. Run python3 /home/s2.py

Deployment for Cluster (bbb-scalelite):

1. Add '--mount type=bind,source=/var/www/,target=/var/www' to the 'SCALELITE_NGINX_EXTRA_OPTS=' string in the file /etc/default/scalelite on the load balancer
2. Add to the each one of your cluster nodes the next script:
> #/bin/bash
> 
> cd /var/bigbluebutton/recording/raw/
> 
> for i in *;
> do
>     mkdir /mnt/scalelite-recordings/var/bigbluebutton/stat/$i;
>     cp $i/events.xml /mnt/scalelite-recordings/var/bigbluebutton/stat/$i/events.xml
> done

3. Add the cronjob for nodes:
> #Copy events.xml to /mnt/ disk every hour, every day
> 00 9-21 * * * /bin/bash /home/copy_events.sh >> /var/log/copy_events.log

Deployment playbook for Ansible:

Coming soon...

