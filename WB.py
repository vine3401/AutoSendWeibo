# -*- coding: utf-8 -*-

import time
import datetime
from WB.wb_login import login
from WB.wb_get_data import get_data
from WB.wb_send import send_wb

(session, uid) = login("18482065251", "Lz122521#")
print("进程启动：")
(text, url_pic) = get_data()
send_wb(session, "进程重启，发送测试验证************\n"+text, url_pic)
while True:
    t = time.localtime(time.time())
    if t.tm_sec == 0 and t.tm_min == 0 and t.tm_hour == 8:
        (text, url_pic) = get_data()
        send_wb(session, "早安！世界\n"+text, url_pic)
    elif t.tm_sec == 0 and t.tm_min == 0 and t.tm_hour == 23:
        (text, url_pic) = get_data()
        send_wb(session, "午安！世界\n"+text, url_pic)
    elif t.tm_sec == 0 and t.tm_min == 25 and t.tm_hour == 12:
        (text, url_pic) = get_data()
        send_wb(session, "晚安！世界\n"+text, url_pic)
    else:
        time_stamp = time.time()
        t = time.localtime(time.time())
        future_time_stamp_8 = datetime.datetime(year=t.tm_year, month=t.tm_mon, day=t.tm_mday,
                                                 hour=8, minute=0, second=0).timestamp()
        future_time_stamp_12 = datetime.datetime(year=t.tm_year, month=t.tm_mon, day=t.tm_mday,
                                                 hour=12, minute=25, second=0).timestamp()
        future_time_stamp_23 = datetime.datetime(year=t.tm_year, month=t.tm_mon, day=t.tm_mday,
                                                 hour=23, minute=0, second=0).timestamp()
        now_time_stamp = int(time_stamp)
        if t.tm_hour < 8:
            sec = abs(future_time_stamp_8 - now_time_stamp)
        else:
            sec = abs(future_time_stamp_23 - now_time_stamp)
        time.sleep(sec)
