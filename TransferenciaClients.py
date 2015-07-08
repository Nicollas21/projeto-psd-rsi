# -*- coding: cp1252 -*-
import socket,socketerror

class TransferenciaClient():
    print "Clinte"

    def __init__(self,host):   
          self._host = host   # Endereco IP do Servidor 
          self._port = 57000  # Porta que o Servidor esta
          
          print "Conectando com servidor..."
          self._udp = socketerror.socketError(socket.AF_INET,socket.SOCK_DGRAM)
          self._udp.connect((self._host,self._port ))
          self._udp.setErrorProb(0.1)
          self._udp.settimeout(5)
          self.seq_pacote = 0

    def closeConnection(self):
        print "Download Terminado"
        self._udp.send("#####%XXXXX")
        self._udp.close()

    def sendFile(self,data):
        mensagem = 'NACK'
        while (mensagem is 'NACK'):
            try:
               data_send = data+"%"+str(self.seq_pacote)
               self._udp.sendWithError(data_send)
               mensagem = self._udp.recvWithError(1024)
               print mensagem
               self.seq_pacote += 1
            except socket.timeout:
                print("Error")

    def readFile(self,arquivo,sizePackage):
        print "Abrindo arquivo..."
        arq,index=open(arquivo,'rb'), 0
        data = arq.read(sizePackage)
        while data:
            self.sendFile(data)
            data = arq.read(sizePackage)
        arq.close()
        
            

    

