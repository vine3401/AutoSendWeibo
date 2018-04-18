# -*- coding: utf-8 -*-
import time

from threading import Thread, Event
from config import TIME_SLOG
from weibo.weibo_sender import WeiboSender
from weibo.weibo_getData import getData
from logger import logger


class SendTask(Thread):

    def __init__(self, http, uid):
        Thread.__init__(self)
        self.stopped = Event()
        self.sender = WeiboSender(http, uid)

    def run(self):
        logger.info("start task...")
        t = time.localtime(time.time()).tm_min
        TIME_SLOG = 60 - t
        print("before Send:", t, TIME_SLOG)
        while not self.stopped.wait(TIME_SLOG*60):
            wt = time.localtime(time.time()).tm_min
            self.sendWeibo()
            t = time.localtime(time.time()).tm_min
            TIME_SLOG = 60 - t
            print("after Send:", t, TIME_SLOG)
            print("wait seconds", abs(wt-t))
        self.sendWeibo()
        logger.info("end task...")

    def stop(self):
        self.stopped.set()

    def sendWeibo(self):
        weibo = getData()
        self.sender.send_weibo(weibo)
