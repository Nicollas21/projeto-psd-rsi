# -*- coding: utf-8 -*-
import socket

def printMenu():
        print "\n*****************************"
        print "* 0 - Iniciar Capturas      *"
        print "* 1 - Identificar Coletores *"
        print "* 2 - Suspender Captura     *"
        print "* 3 - Reiniciar Captura     *"
        print "* 4 - sair                  *"
        print "*****************************"

def printColetores(colet):
	print "*****************************"
        print "*         Coletores         *"
        print "*****************************"

	for indice in colet:
		print "Nome Coletor: "+indice+"\tIP: "+colet[indice]



coletores = {};
laco = True;

AMOUNT_BYTES = 1024

BROADCAST_PORT_SEND = 9000
BROADCAST_PORT_RECV = 9001
BROADCAST_LISTEN = ''
BROADCAST_SEND = '<broadcast>'

bsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
bsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
bsock.bind((BROADCAST_LISTEN,BROADCAST_PORT_RECV))
bsock.settimeout(3)


while (laco == True):
	printMenu();
        data = raw_input('Escolha uma opção: ');

        if data == '0':
                bsock.sendto('iniciar_captura', (BROADCAST_SEND, BROADCAST_PORT_SEND));

	elif data == '1':
		coletore = {};
		bsock.sendto('identificacao', (BROADCAST_SEND, BROADCAST_PORT_SEND));
		try:
                        while True :
                                message , address = bsock.recvfrom(AMOUNT_BYTES)
				coletores[message] = format(address[0]);
		except socket.timeout:
			printColetores(coletores);

	elif data == '2':
		if(len(coletores) == 0):
			print("Favor identificar os coletores.\n");
		else:
			coletor = raw_input('Digite apenas o nome do coletor para suspender a coleta: ');
			if coletores.has_key(coletor):
				bsock.sendto('suspender', (coletores[coletor] ,BROADCAST_PORT_SEND));
			else:
				print "Nome de coletor inexistente."
	elif data == '3':
		if((len(coletores) == 0)):
			print("Favor identificar os coletores.\n");
		else:
			coletor = raw_input('Digite apenas o nome do coletor para reiniciar a coleta: ');
			if coletores.has_key(coletor):
				bsock.sendto('reiniciar', (coletores[coletor] , BROADCAST_PORT_SEND));
			else:
				print "Nome de coletor inexistente."
	elif data == '4':
		laco = False;
		bsock.close();
		print ("Bye");
	else:
		print ("Opção Inválida.\n");
