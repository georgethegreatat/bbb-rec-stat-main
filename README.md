BigBlueButton Recordings Statistic

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

Coming Soon...

Deployment playbook for Ansible:

Coming soon...

