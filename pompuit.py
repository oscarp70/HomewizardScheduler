#!/usr/bin/python3

from crontab import CronTab
import datetime
import os
import http.client, urllib
import requests

my_cron = CronTab(user='root')
  for job in my_cron:
    if job.comment[:7] == 'pompUit':
      my_cron.remove(job)
      my_cron.write()

conn = http.client.HTTPSConnection("api.pushover.net:443")
conn.request("POST", "/1/messages.json",
  urllib.parse.urlencode({
    "token": "a9j857te5yvzowjtouxu6gh1wjmgkp",
    "user": "uWME3CuJe4EZqiRKHmX5T3nQ92WzUy",
    "message": "Pomp Uit",
  }), { "Content-type": "application/x-www-form-urlencoded" })
conn.getresponse()

