#!/usr/bin/env bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

export DISPLAY=:0
nohup /usr/bin/python3 /home/pi/Public/xfinity-usage-monitor/src/xfinity_monitor.py >> /home/pi/Public/cron_xfinity.log 2>&1
