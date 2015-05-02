# -*- coding: cp1252 -*-
from socket import *

serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

serverName = '<broadcast>'

message= ""
while message.upper() != "EXIT":
    #Recebe mensagem do usuario e envia ao destino
    message = raw_input('>>>')
    clientSocket.sendto(message,(serverName, serverPort))

    #Aguarda mensagem de retorno e a imprime
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print("Retorno do Servidor:"+modifiedMessage+" "+str(serverAddress))

clientSocket.close()
