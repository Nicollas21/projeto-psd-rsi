# -*- coding: utf-8 -*-

from ClassificaPkt import *
from ReceiveCommand import *
from threading import Thread


k = ReceiveCommand()
t1 = Thread(target=k.startListen,args=())
t1.start()

