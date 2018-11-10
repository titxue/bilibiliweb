# -*- coding:utf8 -*-
from threading import Thread,Lock

class Mythread(Thread):
    """重写多线程类"""
    def __init__(self, func, args, name=""):
        Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name

    def run(self):
        self.func(self.args)

#线程锁
def lock():
    return Lock()
