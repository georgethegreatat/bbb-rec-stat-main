#!/bin/bash

echo Moving files..

mkdir /var/www/stat/
mkdir /var/www/stat/stat/
mkdir /var/www/stat/stat/css/
mkdir /var/www/stat/stat/Front/fonts/font-awesome/
mkdir /var/www/stat/stat/Front/images/
mkdir /var/www/stat/stat/Front/js/
mkdir /var/www/stat/stat/json-files/
mv Nginx/s2.nginx /etc/bigbluebutton/nginx/s2.nginx
mv Back/s2.py /home/s2.py
mv Front/css /var/www/stat/stat/css/
mv Front/fonts/font-awesome/ /var/www/stat/stat/fonts/font-awesome/
mv Front/images/ /var/www/stat/stat/images/
mv Front/js/ /var/www/stat/stat/js/
mv Front/json-files/ /var/www/stat/stat/json-files/

echo Finished.

echo Install requirements...

pip3 install -r requirements.txt

echo Install Apache modules...

apt install apache2-utils -y

echo Restart Nginx...

service nginx restart

echo Finished successfully.


