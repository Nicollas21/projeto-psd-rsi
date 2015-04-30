# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pika
import sys
import pcap, dpkt, re

class ClassificaPkt():
    protocols = {"bittorrent":"","dhcp":"","http":"","ssdp":"","ssh":"","ssl":""}

    maxPkts = 100
    cnt = {"bittorrent":0,"dhcp":0,"http":0,"ssdp":0,"ssh":0,"ssl":0,"noClass":0}
    #contadores
    cNonIP = 0
    cNonIP = 0
    
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
        
        self.protocols = {"bittorrent":bittorrent,"dhcp":dhcp,"http":http,"ssdp":ssdp,"ssh":ssh,"ssl":ssl}

    def get_protocol_trans_tcp(self,app,eth,ts):
        found = False
        for p in self.protocols.items():
            if p[1].search(app):
                tamanho = len(eth)
                tupla = (tamanho,ts,"eth","ip","tcp",p[0])
                self.enviar_pkt(tupla)
                self.cnt[p[0]] += 1
                found = True
        if (not found):
            self.cnt["noClass"] += 1

    def get_protocol_trans_udp(self,app,eth,ts):
        found = False
        for p in self.protocols.items():
            if p[1].search(app):
                tamanho = len(eth)
                tupla = (tamanho,ts,"eth","ip","udp",p[0])
                self.enviar_pkt(tupla)
                self.cnt[p[0]] += 1
                found = True
        if (not found):
            self.cnt["noClass"] += 1
        
    def classificar_protocol(self, protocols):
        
        for ts, pkt in pcap.pcap('test-capture.pcap'):
            
            
            eth = dpkt.ethernet.Ethernet(pkt) #extraindo dados do pacote
            ip = eth.data
            if isinstance(ip,dpkt.ip.IP):
                    transp = ip.data
                    if isinstance(transp,dpkt.tcp.TCP):
                        app = transp.data.lower()
                        self.get_protocol_trans_tcp(app,eth,ts)
                    elif isinstance(transp,dpkt.udp.UDP):
                        app = transp.data.lower()
                        self.get_protocol_trans_udp(app,eth,ts)
                            
            else:
                    self.cNonIP += 1

            
        for p in self.cnt.items():
            print(p[0]+" Pkts:"+str(p[1]))
        print("Non IP Pkts:"+str(self.cNonIP))

    def enviar_pkt(self,tupla):
        #print tupla

        tupla = str(tupla)
        tupla = tupla.replace(" ","")
        tupla = tupla.replace("(","")
        tupla = tupla.replace(")","")
        tupla = tupla.replace("''","")
        teste = tupla.split(',')
        nome_protocolo = str(teste[5].replace("'",""))
        #print teste[5].replace("'","")
        
        credentials = pika.PlainCredentials('server', 'server123')
        connection = pika.BlockingConnection(pika.ConnectionParameters(
               '172.16.205.153', 5672, 'grupo1', credentials))
        channel = connection.channel()

        channel.exchange_declare(exchange='topic_logs',
                         type='topic')

        routing_key = nome_protocolo if len(teste) > 1 else 'anonymous.info'
        print routing_key
        message = str(teste) or 'Hello World!'
        channel.basic_publish(exchange='topic_logs',
                      routing_key=routing_key,
                      body=message)
        print " [x] Sent %r:%r" % (routing_key, message)
        connection.close()
            
        
