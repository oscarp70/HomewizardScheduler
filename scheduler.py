#!/usr/bin/python3

from flask import Flask, render_template, request, url_for
from crontab import CronTab
import datetime
import time
import http.client, urllib
import requests
import configparser
from distutils.util import strtobool
import pycurl
from io import BytesIO

config = configparser.ConfigParser()
config.sections()
config.read('scheduler.ini')

homewizard_address = config['ACTION']['homewizard_address']
homewizard_password = config['ACTION']['homewizard_password']
homewizard_port = config['ACTION']['homewizard_port']
switch = config['ACTION']['switch']
server_port = config['SERVER']['port']
offset = config['SERVER']['offset']
debug = config['SERVER']['debug']
python_path = config['PATHS']['python']
app_path = config['PATHS']['app']

app = Flask(__name__)

@app.route("/")
def index():
  my_time = "time"
  my_url = "index.html"
  my_cron = CronTab(user='root')
  for job in my_cron:
    if job.comment[:9] == 'actionOff':
        my_time = datetime.datetime.strptime(job.comment[10:29], '%Y-%m-%d %H:%M:%S')        
        my_timestamp = datetime.datetime.timestamp(my_time)
        now = datetime.datetime.now()
        now_timestamp = datetime.datetime.timestamp(now)
        if my_timestamp < now_timestamp:
          my_cron.remove(job)
          my_cron.write()
          my_url="index.html"
        else:
          my_url="timer.html"
    else:
        my_url="index.html"
  return render_template(my_url, my_time=my_time, offset=offset)

@app.route("/timer/", methods=['POST'])
def schedule_timer():
   delta_h = int(request.form["hours"]) 
   delta_m = int(request.form["minutes"])
   action_now = request.form.get('actionOn')
   if action_now:
     b_obj = BytesIO()
     crl = pycurl.Curl()
     crl.setopt(crl.URL, f'http://{homewizard_address}:{homewizard_port}/{homewizard_password}/sw/{switch}/on')
     crl.setopt(crl.WRITEDATA, b_obj)
     crl.perform()
     crl.close()
     time.sleep(1)
   my_time = datetime.datetime.now() + datetime.timedelta(hours=delta_h, minutes=delta_m)
   hours = my_time.hour
   minutes = my_time.minute
   my_cron = CronTab(user='root')
   for job in my_cron:
     if job.comment[:9] == 'actionOff':
        my_cron.remove(job)
        my_cron.write()
   job = my_cron.new(command=f'sudo {python_path} {app_path}/actionOff.py > {app_path}/cronlog 2>&1' , comment=f'actionOff {my_time}')
   job.setall(f'{minutes} {hours} * * *')   
   my_cron.write()
   return render_template('timer.html', my_time=my_time, offset=offset);

@app.route("/back/", methods=['POST'])
def back():
  my_cron = CronTab(user='root')
  for job in my_cron:
      if job.comment[:9] == 'actionOff':
        my_cron.remove(job)
        my_cron.write()
  b_obj = BytesIO()
  crl = pycurl.Curl()
  crl.setopt(crl.URL, f'http://{homewizard_address}:{homewizard_port}/{homewizard_password}/sw/{switch}/off')
  crl.setopt(crl.WRITEDATA, b_obj)
  crl.perform()
  crl.close()
  time.sleep(1)
  return render_template('index.html')

if __name__ == "__main__": 
    app.run(debug=bool(strtobool(debug)), host="0.0.0.0", port=int(f'{server_port}'))
