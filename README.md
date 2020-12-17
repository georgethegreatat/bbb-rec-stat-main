BBBRSS - BigBlueButton Recordings Statistic Script

Deployment for one server (not cluster):

1. cd /root
2. git clone https://github.com/georgethegreatat/bbb-rec-stat-main/
3. chmod a+x update.sh
4. ./update.sh
5. Put into crontab (if you're not 'vi' fun you can use 'EDITOR=nano crontab -e' command):
#BigBlueButton stat script rerunning every hour (09-21, each day)
> 00 09-21 * * * python3 /home/s2.py >> /var/log/bbb-stat.log
6. Creat file '.bbb-key' in /home/ directory and put there your bbb shared secret key (only key, without BBB_KEY etc), close and save.
7. Run python3 /home/s2.py

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

