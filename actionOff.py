#!/usr/bin/python3

from crontab import CronTab
import datetime
import time
import http.client, urllib
import configparser
from distutils.util import strtobool
import pycurl
from io import BytesIO
import os
import sys

#sys.path.append(os.path.abspath("/home/oscarp/.local/lib/python3.6/site-packages/crontab.py"))

config = configparser.ConfigParser()
config.sections()
config_file = os.path.join(os.path.dirname(__file__), 'scheduler.ini')
config.read(config_file)

homewizard_address = config['ACTION']['homewizard_address']
homewizard_password = config['ACTION']['homewizard_password']
homewizard_port = config['ACTION']['homewizard_port']
switch = config['ACTION']['switch']
pushover = config['PUSHOVER']['enabled'] 
token = config['PUSHOVER']['token']
user = config['PUSHOVER']['user']
message = config['PUSHOVER']['message']

b_obj = BytesIO()
crl = pycurl.Curl()
crl.setopt(crl.URL, f'http://{homewizard_address}:{homewizard_port}/{homewizard_password}/sw/{switch}/off')
crl.setopt(crl.WRITEDATA, b_obj)
crl.perform()
crl.close()
time.sleep(1)

my_cron = CronTab(user='root')
for job in my_cron:
  if job.comment[:9] == 'actionOff':
      my_cron.remove(job)
      my_cron.write()

if bool(strtobool(pushover)):
  conn = http.client.HTTPSConnection("api.pushover.net:443")
  conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
      "token": token,
      "user": user,
      "message": message,
    }), { "Content-type": "application/x-www-form-urlencoded" })
  conn.getresponse()

