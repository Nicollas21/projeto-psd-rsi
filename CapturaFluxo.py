# -*- coding: utf-8 -*-
import pika
import pcap, dpkt, re, time
from threading import *
from Log import *
import sys

class CapturaFluxo():
        erro = Logs()
        #Criar identificador Captura
        #contadores
        cNonIP = 0
        cUDP = 0
        cTCP = 0
        cnt = 0
        
        #Dicionarios
        protocols = {"bittorrent":"","dhcp":"","http":"","ssdp":"","ssh":"","ssl":""}
        fluxos= {}
        timers={}
        TIMER = 2
        nomeColetor = ''
        start_captura = True

        def nome_Coletor(self,nome):
                self.nomeColetor = nome
        
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
                

        def status_captura(self,status):
                self.start_captura = status
                
        def capturar_pkts(self):
                try:
                        for ts, pkt in pcap.pcap():
                                if self.start_captura is True:
                                        eth = dpkt.ethernet.Ethernet(pkt) #extraindo dados do pacote
                                        ip = eth.data
                                        if isinstance(ip,dpkt.ip.IP):
                                                Ip_src = ip.src
                                                Ip_dst = ip.dst
                                                protocol = ip.p
                                                if isinstance(ip.data,dpkt.tcp.TCP) or isinstance(ip.data,dpkt.udp.UDP):
                                                        Port_src = ip.data.dport
                                                        Port_dest = ip.data.sport

                                                        #Gerar chave e tupla para enviar para o dic de fluxos       
                                                        chave = (Ip_src,Ip_dst,Port_src,Port_dest,protocol)

                                                        if not chave in self.fluxos:
                                                                self.fluxos[chave] = [(ts,ip)]
                                                                self.temporizador(chave)
                                                        else:
                                                                self.fluxos[chave].append((ts,ip))
                                                                self.temporizador(chave)
                       
                                                if isinstance(ip.data,dpkt.tcp.TCP):
                                                        self.cTCP += 1
                                                elif isinstance(ip.data,dpkt.udp.UDP):
                                                        self.cUDP += 1
                                        else:
                                                self.cNonIP += 1

                                else:
                                        break
                                      
                        print("IP Pkts:"+str(self.cTCP+self.cUDP))
                        print("Non IP Pkts:"+str(self.cNonIP))
                        
                        
                except:
                        self.erro.setError(sys.exc_info()[1],self.nomeColetor)
                        print self.erro.getError()  
        
        def temporizador(self,chave):
                if chave in self.timers:
                        self.timers[chave].cancel()
                self.timers[chave] = Timer(self.TIMER,self.close_flow,args=[chave])
                self.timers[chave].start()

        def close_flow(self,chave):
                #print(chave)
                self.create_tupla(self.fluxos[chave])
                del(self.fluxos[chave])
                        
        def calc_dur(self,pkts): #pkts is the packet list of a flow, and each element is a tuple (ts,pkt)
                first = pkts[0]
                last = pkts[-1]
                dur = last[0] - first[0]
                return dur
                

        def calc_size(self, pkts): #pkts is the packet list of a flow, and each element is a tuple (ts,pkt)
                #print reduce(lambda x,y: x+y, pkts)
                lista=[]
                for i in pkts:
                        lista.append(i[1].len)                       
                return sum(lista)
        
        def classify(self,pkts):
                for pkt in pkts:
                        app = pkt[1].data.data.lower()
                        Protocol_found = ""
                        for p in self.protocols.items(): #Checar qual o protocolo
                                if p[1].search(app):
                                        Protocol_found = p[0]
                        if Protocol_found:
                                return Protocol_found
                else:
                        return "unknown"

        def create_tupla(self,pkts):
                self.dur = self.calc_dur(pkts)
                self.dur = (self.dur*0.001) #conversão para seg

                self.size = self.calc_size(pkts)
                self.size = self.size/1024.0 #conversão para Kb

                self.classi = self.classify(pkts[0:5])

                if self.dur == 0 or self.size == 0:
                          pass    
                else:
                        self.rate = self.size/self.dur #taxa Kb/s
                        tupla = (self.classi,self.dur,self.size,self.rate)
                        #tupla = (self.classi,self.dur,self.size)
                        print tupla
                        #self.send_tupla(self.classi,tupla)

        def send_tupla(self,nome_protocolo,msg):
        
                credentials = pika.PlainCredentials('server', 'server123')
                connection = pika.BlockingConnection(pika.ConnectionParameters(
                       'localhost', 5672, 'grupo1', credentials))
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

