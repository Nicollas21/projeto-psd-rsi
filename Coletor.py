# -*- coding: cp1252 -*-
import socket
import os, time
import threading, Queue
from TransferenciaClients import *
from CapturaFluxo import *
import sys
from Log import *


class Coletor(threading.Thread):
	def __init__(self):
		super(Coletor, self).__init__();
		self.stoprequest = threading.Event();
	        self.pauserequest = threading.Event();

	        self.cap = CapturaFluxo();
                #Assinar Protocolos
                self.bit = self.cap.get_arquivo('l7-pat/bittorrent.pat');
                self.dhcp = self.cap.get_arquivo('l7-pat/dhcp.pat');
                self.http = self.cap.get_arquivo('l7-pat/http.pat');
                self.ssdp = self.cap.get_arquivo('l7-pat/ssdp.pat');
                self.ssh = self.cap.get_arquivo('l7-pat/ssh.pat');
                self.ssl = self.cap.get_arquivo('l7-pat/ssl.pat');
                self.cap.assinar_protocols(self.bit,self.dhcp,self.http,self.ssdp,self.ssh,self.ssl);		
                self.cap.nome_Coletor('sul')
                
    	def run(self):
                while not self.stoprequest.isSet():
			if not self.pauserequest.isSet():
                                self.cap.capturar_pkts()

	def stop(self, timeout=None):
        	self.stoprequest.set()
	        super(Coletor, self).join(timeout)

   	def pause(self, timeout=None):
        	self.pauserequest.set()
        	self.cap.status_captura(False)

	def resume(self, timeout=None):
        	self.pauserequest.clear()
        	self.cap.status_captura(True)
	        	   
def main():
	t = Coletor();
	t.start();
	erro = Logs();
	
	try:
		nome_coletor = 'sul' # Para cada coletor, o nome tem que ser diferente
		status = 'coletando';
			
		AMOUNT_BYTES = 1024;
		BROADCAST_PORT = 9000;
            	BROADCAST_LISTEN = '';          

            	bsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
            	bsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            	bsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            	bsock.bind((BROADCAST_LISTEN, BROADCAST_PORT))

            	print "Agardando.."
			
		while True :
                	message , address = bsock.recvfrom(AMOUNT_BYTES);
			print("message '{0}' from : {1}".format(message, address));
			if message == 'download':
                                arq = "logs_"+nome_coletor+".txt"
                                print arq
                                obj = TransferenciaClient(address[0]);
				obj.readFile(arq,50);
				obj.closeConnection();
				pass;
                	elif message == 'identificacao':
				bsock.sendto(nome_coletor+'-'+status, (address[0] ,BROADCAST_PORT));
        	        elif message == 'suspender':
				#Colocar aq a funcao que ira suspernder a coleta
				print "Coletor "+nome_coletor+" suspenso";
				status = 'suspenso';
				t.pause();
			elif message == 'reiniciar':
				print "Coletor "+nome_coletor+" reiniciado";
				status = 'coletando';
				t.resume();

        except:
            erro.setError(sys.exc_info()[1],nome_coletor);
            print erro.getError();
	
if __name__ == '__main__':
    main()






	

