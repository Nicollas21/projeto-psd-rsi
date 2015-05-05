# -*- coding: utf-8 -*-

from ClassificaPkt import *
from ReceiveCommand import *
from threading import Thread


k = ReceiveCommand()

y = ClassificaPkt()
bit = y.get_arquivo('l7-pat/bittorrent.pat')
dhcp = y.get_arquivo('l7-pat/dhcp.pat')
http = y.get_arquivo('l7-pat/http.pat')
ssdp = y.get_arquivo('l7-pat/ssdp.pat')
ssh = y.get_arquivo('l7-pat/ssh.pat')
ssl = y.get_arquivo('l7-pat/ssl.pat')
protocol = y.assinar_protocols(bit,dhcp,http,ssdp,ssh,ssl)


t1 = Thread(target=k.startListen,args=())
t1.start()
"""
t2 = Thread(target=y.classificar_protocol,args=(protocol,"",))
t2.start()
"""
