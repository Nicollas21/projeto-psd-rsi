# -*- coding: cp1252 -*-
import socket


class ReceiveCommand():
    nome_coletor = 'norte' # Para cada coletor, o nome tem que ser diferente

    AMOUNT_BYTES = 1024

    BROADCAST_PORT_SEND = 9001      # Porta que o cliente estará escutando
    BROADCAST_PORT_RECV = 9000      # Porta que o cliente irá enviar mensagem
    BROADCAST_LISTEN = ''           

    bsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
    bsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    bsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    bsock.bind((BROADCAST_LISTEN, BROADCAST_PORT_RECV))

    print "Agardando.."

    while True :
        message , address = bsock.recvfrom(AMOUNT_BYTES);
        print("message '{0}' from : {1}".format(message, address));
        if message == 'identificacao':
            bsock.sendto(nome_coletor, (address[0] ,BROADCAST_PORT_SEND));
        elif message == 'suspender':
            #Colocar aq a funcao que ira suspernder a coleta
            print "Coletor "+nome_coletor+" suspenso";
        elif message == 'reiniciar':
            #Colocar aq a funcai que ira reiniciar a coleta
            print "Coletor "+nome_coletor+" reiniciado";
                    


                    
                
                    
                
