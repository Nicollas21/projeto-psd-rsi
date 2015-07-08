# -*- coding: cp1252 -*-
import os, time
import threading, Queue
import pika

import numpy as np
import matplotlib.pyplot as plt

class Gerente(threading.Thread):
	def __init__(self):
		super(Gerente, self).__init__();
		self.stoprequest = threading.Event();
		
		self.protocolos = {};
		
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                        host='localhost'))
                self.channel = self.connection.channel()

                self.channel.queue_declare(queue='dados')
		

    	def run(self):
		while not self.stoprequest.isSet():
			self.consumir_fila();
						

	def callback(self,ch, method, properties, body):
                if not body in self.protocolos:
                        self.protocolos[body] = 1
                else:
                        self.protocolos[body]+=1


        def consumir_fila(self):            
                self.channel.basic_consume(self.callback, queue='dados', no_ack=True)
                self.channel.start_consuming()
                #print self.protocolos

        def mostrar(self):
                for key in self.protocolos.items():
                        print key[0],":",key[1]

	def stop(self, timeout=None):
        	self.stoprequest.set()
        	self.connection.close()
	        super(Gerente, self).join(timeout)

	def consultaProtocolo(self,name):
                dic_temp={'Rato':0, 'Elefante':0,'Tartarugas':0,'Libelulas':0,'Guepardos':0,'Caramujos':0}
                for key,cont in self.protocolos.items():
                        proto,animal = key.split(",")
                        if proto.lower() == name.lower():
                                print animal,":",cont
                                dic_temp[animal]=cont

                self.showGrafic(dic_temp)

        def consultaTotal(self):
                dic_temp={'Rato':0, 'Elefante':0,'Tartarugas':0,'Libelulas':0,'Guepardos':0,'Caramujos':0}
                for key,cont in self.protocolos.items():
                        proto,animal = key.split(",")
                        print animal,":",cont
                        dic_temp[animal]=cont

                self.showGrafic(dic_temp)

        def showGrafic(self,dic):
                #colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'grey', 'green', 'white']
                laco = True
                while (laco == True):
                        print u"Escolha uma Metrica: (1)Tamanho (2)Dura��o (3)Taxa (4)Menu "
                        data = raw_input('Escolha uma Metrica: ');
                        
                        if data == '1':
                                labels = 'Rato', 'Elefante'
                                sizes = [dic['Rato'], dic['Elefante']]
                                colors = ['yellowgreen', 'gold']
                                explode = (0.1, 0)
                                plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                                        autopct='%1.1f%%', shadow=True, startangle=90)
                                plt.title('Analise Tamanho')
                                plt.axis('equal')
                                plt.show()
        
                        elif data == '2':
                                labels= 'Tartarugas','Libelulas'
                                sizes = [dic['Tartarugas'], dic['Libelulas']]
                                colors = ['lightskyblue', 'lightcoral']
                                explode = (0.1, 0)
                                plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                                        autopct='%1.1f%%', shadow=True, startangle=90)
                                plt.title(u'Analise Dura��o')
                                plt.axis('equal')
                                plt.show()
                                
                        elif data == '3':
                                labels= 'Guepardos','Caramujos'
                                sizes = [dic['Guepardos'], dic['Caramujos']]
                                colors = ['grey', 'green']
                                explode = (0.1, 0)
                                plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                                        autopct='%1.1f%%', shadow=True, startangle=90)
                                plt.title('Analise Taxa')
                                plt.axis('equal')
                                plt.show()

                        elif data == '4':
                                break
                                
                        else:
                                print ("Opção Inválida.\n");
			
		
	
def printMenu():
        print "\n****************************"
        print "* 1 - Mostrar Contadores     *"
        print "* 2 - Consulta Protocolo     *"
        print "* 3 - Consulta Total         *"
        print "* 4 - Sair                   *"
        print "******************************"
    
def main():
	t = Gerente();
	t.start()
	laco = True;
	while (laco == True):
		printMenu();
		data = raw_input('Escolha uma opção: ');
		
		if data == '1':
			t.mostrar();
		
		elif data == '2':
                        print u"Escolha um Protocolo: bittorrent - http - dhcp - ssdp - ssh - ssl - unknown"
			protocolo = raw_input('Digite o nome do protocolo: ');
                        if (protocolo=='bittorrent' or protocolo=='http' or protocolo=='dhcp' or protocolo=='ssdp' or protocolo=='ssh' or protocolo=='ssl'or
                            protocolo=='unknown'):
                                t.consultaProtocolo(protocolo);
                        else:
                                print "Protocolo Invalido!"
			
		elif data == '3':
                        t.consultaTotal()
		elif data == '4':
			t.stop();	
			laco = False;
			print ("Bye");
			
		else:
			print ("Opção Inválida.\n");
	

if __name__ == '__main__':
    main()






	

