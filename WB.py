# -*- coding: utf-8 -*-

import time

from WB.wb_login import login
from WB.wb_get_data import get_data
from WB.wb_send import send_wb

(session, uid) = login("18482065251", "Lz122521#")
print("进程启动：")
(text, url_pic) = get_data()
send_wb(session, "进程重启，发送测试验证", url_pic)
while True:
    t = time.localtime(time.time())
    if t.tm_sec == 0 and t.tm_min == 0:
        print("发送微博Exception")
        (text, url_pic) = get_data()
        send_wb(session, text, url_pic)
    else:
        t = time.localtime(time.time())
        sec = 60 - t.tm_sec + (60-t.tm_min-1)*60
        time.sleep(sec)
