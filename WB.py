# -*- coding: utf-8 -*-
import os
import sys
import time
from datetime import datetime
from os import path as osp

import yaml
from apscheduler.schedulers.blocking import BlockingScheduler

from WB.wb_login import login
from WB.wb_get_data import get_data
from WB.wb_send import send_wb

yaml_path = osp.join(osp.dirname(osp.realpath(__file__)), 'config.yaml')
if osp.exists(yaml_path):
    with open(yaml_path) as ysettings:
        locals().update(yaml.load(ysettings))

def send_job():
    (session, uid) = login(username, password)
    msg = ""
    if datetime.now().hour == 8:
        msg = "早"
    elif datetime.now().hour == 12:
        msg = "午"
    elif datetime.now().hour == 23:
        msg = "晚"
    (text, url_pic) = get_data()
    message = msg+("安！世界\n") + text
    send_wb(session, message, url_pic)
    session.close()

if __name__ == '__main__':
    print("name:",sys.argv[0])  
    for i in range(1,len(sys.argv)):  
        print("parameter",i,sys.argv[i])
    scheduler = BlockingScheduler()
    scheduler.add_job(send_job, 'cron', hour="8, 23")
    scheduler.add_job(send_job, 'cron', hour="12", minute="25")
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

        
