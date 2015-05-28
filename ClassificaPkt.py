# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pika
import sys
import pcap, dpkt, re

class ClassificaPkt():
    protocols = {"bittorrent":"","dhcp":"","http":"","ssdp":"","ssh":"","ssl":""}

    maxPkts = 100
    cnt = {"bittorrent":0,"dhcp":0,"http":0,"ssdp":0,"ssh":0,"ssl":0,"unknown":0}
    #contadores
    cNonIP = 0
    message = "nada"
    
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

    def get_protocol_trans(self,app,eth,ts,transp):
        found = False
        tamanho = len(eth)
        for p in self.protocols.items():
            if p[1].search(app):
                tupla = tamanho,ts,"eth","ip",transp,p[0]
                self.modifier_tupla(tupla)
                self.cnt[p[0]] += 1
                found = True
            if (not found):
                self.cnt["unknown"] += 1
                tupla = tamanho,ts,"eth","ip",transp,"unknown"
                self.modifier_tupla(tupla)
        
    def classificar_protocol(self):
        #nPkts=0
        
        for ts, pkt in pcap.pcap("test-capture.pcap"):
            #nPkts += 1
                
            eth = dpkt.ethernet.Ethernet(pkt) #extraindo dados do pacote
            ip = eth.data
            if isinstance(ip,dpkt.ip.IP):
                    transp = ip.data
                    if isinstance(transp,dpkt.tcp.TCP):
                        app = transp.data.lower()
                        tcp = "tcp"
                        self.get_protocol_trans(app,eth,ts,tcp)
                    elif isinstance(transp,dpkt.udp.UDP):
                        app = transp.data.lower()
                        udp = "udp"
                        self.get_protocol_trans(app,eth,ts,udp)
                                
            else:
                    self.cNonIP += 1
		    tamanho = len(eth)
                    tupla = tamanho,ts,"eth","unknown","unknown","unknown"
                    self.modifier_tupla(tupla)

            #if (nPkts == self.maxPkts):
                    #break
                
        for p in self.cnt.items():
            print(p[0]+" Pkts:"+str(p[1]))
        print("Non IP Pkts:"+str(self.cNonIP))

    def modifier_tupla(self,tupla):
        #print type(tupla[0])
        if type(tupla[0]) is int:
            tupla = str(tupla)
            tupla = tupla.replace(" ","")
            tupla = tupla.replace("(","")
            tupla = tupla.replace(")","")
            teste = tupla.split(',')
            nome_protocolo = str(teste[5].replace("'",""))
            #print nome_protocolo
            print teste
            #self.envia_tupla(nome_protocolo,teste)
            
    def envia_tupla(self,nome_protocolo,msg):
        
        credentials = pika.PlainCredentials('server', 'server123')
        connection = pika.BlockingConnection(pika.ConnectionParameters(
               '172.16.205.153', 5672, 'grupo1', credentials))
        channel = connection.channel()

        channel.exchange_declare(exchange='topic_logs',
                         type='topic')

        routing_key = nome_protocolo if len(msg) > 1 else 'anonymous.info'
        print routing_key
        message = str(msg) or 'Hello World!'
        channel.basic_publish(exchange='topic_logs',
                      routing_key=routing_key,
                      body=message)
        print " [x] Sent %r:%r" % (routing_key, message)
        connection.close()
        
        
