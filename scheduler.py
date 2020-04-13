#!/usr/bin/python3

from flask import Flask, render_template, request, url_for
from crontab import CronTab
import datetime
import os
import http.client, urllib
import requests

app = Flask(__name__)

@app.route("/")
def index():
  my_time = "time"
  my_cron = CronTab(user='root')
  for job in my_cron:
    if job.comment[:7] == 'pompUit':
        my_time = datetime.datetime.strptime(job.comment[8:27], '%Y-%m-%d %H:%M:%S')        
        now = datetime.datetime.now()
        now_timestamp = datetime.datetime.timestamp(now)
        my_timestamp = datetime.datetime.timestamp(my_time)
        print(f'nu: {now_timestamp} en cron: {my_timestamp}')
        print(f'Tijd in cron: {my_time}')
        if my_timestamp < now_timestamp:
          my_cron.remove(job)
          my_cron.write()
          my_url="index.html"
        else:
          my_url="timer.html"
    else:
        my_url="index.html"
  return render_template(my_url, my_time=my_time)

@app.route("/timer/", methods=['POST'])
def schedule_timer():
   os.system('~/pompAan.sh')
   delta_u = int(request.form["uren"])+2
   delta_m = int(request.form["minuten"])
   my_time = datetime.datetime.now() + datetime.timedelta(hours=delta_u, minutes=delta_m)
   uren = my_time.hour
   minuten = my_time.minute
   my_cron = CronTab(user='root')
   for job in my_cron:
     if job.comment[:7] == 'pompUit':
        my_cron.remove(job)
        my_cron.write()
   job = my_cron.new(command='/home/oscarp/scheduler/pompUit.sh' , comment=f'pompUit {my_time}')
   job.setall(f'{minuten} {uren} * * *')   
   my_cron.write()
   print(f'Scheduler tijd: {my_time}')
   return render_template('timer.html', my_time=my_time);

@app.route("/terug/", methods=['POST'])
def back():
  my_cron = CronTab(user='root')
    for job in my_cron:
      if job.comment[:7] == 'pompUit':
        my_cron.remove(job)
        my_cron.write()

  r =requests.get('http://192.168.178.100:85/geheim/sw/9/off')

 return render_template('index.html')

if __name__ == "__main__": 
    app.run(debug=True, host="0.0.0.0", port=8095)   

