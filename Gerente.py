# -*- coding: cp1252 -*-
import socket
import os, time
import threading, Queue
from TransferenciaServer import *

class Gerente(threading.Thread):
	def __init__(self):
		super(Gerente, self).__init__();
		self.stoprequest = threading.Event();
		self.mostrarmonitor = threading.Event();
		self.coletores = {};
		
		self.AMOUNT_BYTES = 1024

                self.BROADCAST_PORT = 6000
                self.BROADCAST_LISTEN = ''
                self.BROADCAST_SEND = '<broadcast>'

		self.bsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
		self.bsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.bsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                self.bsock.bind((self.BROADCAST_LISTEN,self.BROADCAST_PORT))
		self.bsock.settimeout(2)
		

    	def run(self):
		while not self.stoprequest.isSet():
			self.identificar();
						
		self.bsock.close();
		#time.sleep(5) #atraso de processamento
		print("Parou")

	def stop(self, timeout=None):
        	self.stoprequest.set()
	        super(Gerente, self).join(timeout)

   	def mostrar(self, timeout=None):
		print "\n\n*****************************"
                print "*         Coletores         *"
                print "*****************************"
		for indice in self.coletores:
			 print "Nome Coletor: "+indice+"\tIP: "+self.coletores[indice]['ip']+"\tSTATUS: "+self.coletores[indice]['status'];

	def suspenderCaptura(self,coletor):
		print "entrou suspencao";
		if self.coletores.has_key(coletor):
			print self.coletores[coletor]['ip'];
			self.bsock.sendto('suspender', (self.coletores[coletor]['ip'] ,self.BROADCAST_PORT));
		else:
			print "Nome de coletor inexistente.";

	def download(self,coletor):
		if self.coletores.has_key(coletor):
			self.bsock.sendto('download', (self.coletores[coletor]['ip'] ,self.BROADCAST_PORT));
			obj = TransferenciaServer();
			obj.receiveFile(coletor);
                        obj.closeConnection();
                else:
                        print "Nome de coletor inexistente."
	
	def reiniciarCaptura(self,coletor):
		if self.coletores.has_key(coletor):
                        self.bsock.sendto('reiniciar', (self.coletores[coletor]['ip'] ,self.BROADCAST_PORT));
                else:
                        print "Nome de coletor inexistente."
		
	def identificar(self):
		self.bsock.sendto('identificacao', (self.BROADCAST_SEND, self.BROADCAST_PORT));
		try:
			while True :
				message , address = self.bsock.recvfrom(self.AMOUNT_BYTES);
				#print message;
				if(message <> 'identificacao' and  message <> 'reiniciar' and message <> 'download' and message <> 'suspender' and message <> 'capturarPkt'):
					valores = message.split("-");
					dicionario = {};
					dicionario['ip'] = format(address[0]);
					dicionario['status'] = valores[1]; 
					self.coletores[valores[0]] = dicionario;
					
		except socket.timeout:
			pass;
			
		
	
def printMenu():
        print "\n*****************************"
        print "* 1 - Mostrar Coletores     *"
        print "* 2 - Suspender Captura     *"
        print "* 3 - Reiniciar Captura     *"
        print "* 4 - Download Logs         *"
        print "* 5 - sair                  *"
        print "*****************************"
    
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
			t.mostrar();
			coletor = raw_input('Digite apenas o nome do coletor para suspender a coleta: ');
			t.suspenderCaptura(coletor);
			
		elif data == '3':
			t.mostrar();
			coletor = raw_input('Digite apenas o nome do coletor para reiniciar a coleta: ');
			t. reiniciarCaptura(coletor);
		
		elif data == '4':
			t.mostrar();
			coletor = raw_input('Digite apenas o nome do coletor para fazer o download: ');
			t.download(coletor);
		
		elif data == '5':
			t.stop();	
			laco = False;
			print ("Bye");
		else:
			print ("Opção Inválida.\n");
	

if __name__ == '__main__':
    main()






	

