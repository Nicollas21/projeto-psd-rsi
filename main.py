# -*- coding: utf-8 -*-

from CapturaPkt import *
from ClassificaPkt import *

#x = CapturaPkt()
#x.getPkt_range(20)

y = ClassificaPkt()
bit = y.get_arquivo('l7-pat/bittorrent.pat')
dhcp = y.get_arquivo('l7-pat/dhcp.pat')
http = y.get_arquivo('l7-pat/http.pat')
ssdp = y.get_arquivo('l7-pat/ssdp.pat')
ssh = y.get_arquivo('l7-pat/ssh.pat')
ssl = y.get_arquivo('l7-pat/ssl.pat')
protocol = y.assinar_protocols(bit,dhcp,http,ssdp,ssh,ssl)

y.classificar_protocol(protocol)
