# -*- coding: utf-8 -*-

import sys
import pcap, dpkt, re

class ClassificaPkt():

    def get_arquivo(self,Dir):
        file = open(Dir).readlines()
        return file

    def assinar_protocols(self, p1, p2, p3, p4, p5, p6):
        expr = p1[1]
        bittorrent = re.compile(expr)

        expr = p2[1]
        dhcp = re.compile(expr)

        expr = p3[1]
        http = re.compile(expr)
        
        expr = p4[1]
        ssdp = re.compile(expr)

        expr = p5[1]
        ssh = re.compile(expr)

        expr = p6[1]
        ssl = re.compile(expr)
        
        protocols = {"bittorrent":bittorrent,"dhcp":dhcp,"http":http,"ssdp":ssdp,"ssh":ssh,"ssl":ssl}

        return protocols
        
    def classificar_protocol(self, protocols):
        maxPkts = 100
        nPkts=0
        cnt = {"bittorrent":0,"dhcp":0,"http":0,"ssdp":0,"ssh":0,"ssl":0,"noClass":0}
        #contadores
        cNonIP = 0
        cNonIP = 0
        
        for ts, pkt in pcap.pcap():
            nPkts += 1
            
            eth = dpkt.ethernet.Ethernet(pkt) #extraindo dados do pacote
            ip = eth.data
            if isinstance(ip,dpkt.ip.IP):
                    transp = ip.data
                    if isinstance(transp,dpkt.tcp.TCP) or isinstance(transp,dpkt.udp.UDP):
                            app = transp.data.lower()
                            found = False
                            for p in protocols.items():
                                    if p[1].search(app):
                                            tupla = (len(app),ts,eth,ip,app)
                                            self.enviar_pkt(tupla)
                                            cnt[p[0]] += 1
                                            found = True
                            if (not found):
                                    cnt["noClass"] += 1
            else:
                    cNonIP += 1

            if (nPkts == maxPkts):
                   break
            
        for p in cnt.items():
            print(p[0]+" Pkts:"+str(p[1]))
        print("Non IP Pkts:"+str(cNonIP))

    def enviar_pkt(self,tupla):
        print tupla
    
