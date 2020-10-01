#!/usr/bin/env bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

export DISPLAY=:0
nohup /usr/bin/python3 /home/pi/Public/xfinity-monitor/src/xfinity_plot.py >> /home/pi/Public/cron.log 2>&1
