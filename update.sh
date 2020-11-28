#/bin/bash

git clone https://github.com/georgethegreatat/bbb-rec-stat-main

echo Moving files..

mkdir /var/www/stat/
mkdir /var/www/stat/stat/
mv Nginx/s2.nginx /etc/bigbluebutton/nginx/s2.nginx
mv Back/s2.py /home/s2.py
mv Front/css /var/www/stat/stat/css/
mv Front/fonts/font-awesome/ /var/www/stat/stat/Front/fonts/font-awesome/
mv Front/images/ /var/www/stat/stat/Front/images/
mv Front/js/ /var/www/stat/stat/Front/js/
mv Front/json-files/ /var/www/stat/stat/json-files/

echo Finished.

echo Install requirements...

pip3 install -r requirements.txt

echo Restart Nginx...

service nginx restart

echo Finished successfully.
