# -*- coding: utf-8 -*-

# Servidor
 
import socket,socketerror

class TransferenciaServer():
    print "Servidor"

    def __init__(self):
        self._hostServer = ''     # Endereco IP do Servidor
        self._portServer = 57000            # Porta que o Servidor esta
        self._udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	self._orig = (self._hostServer, self._portServer)
        print "Escutando a porta..."
        self._udp.bind(self._orig)
        self._nameFile = ''
        self.estado = 0
     

    def receiveFile(self,coletor):
        print "Aguardando o arquivo..."
        nome_arq = "File_ouputt_"+coletor+".txt"
        arq = open(nome_arq,'wb')
        while 1:
            try:
                dados_receive,addr= self._udp.recvfrom(1024)
                msg = dados_receive.split('%')
                dados = msg[0]
                seq_pacote = msg[1]
                
                mensagem = 'ACK'
                if dados == '#####' and seq_pacote == 'XXXXX':
                         break
                else:
                    if (int(seq_pacote) == self.estado):
                        #Enviar Confirmação
                        dados_send = mensagem+"%"+str(self.estado)
                        self._udp.sendto(dados_send,addr)
                        print self.estado
                        #Aplicação
                        #print dados
                        arq.write(dados)
                        self.estado += 1
                    elif (int(seq_pacote) == (self.estado-1)):
                        dados_send = mensagem+"%"+str(self.estado-1)
                        #print dados_send
                        self._udp.sendto(dados_send,addr)
                    
            except (KeyboardInterrupt, SystemExit):
                break
        arq.close()    
        
    def closeConnection(self):
        print "Download Terminado"
        self._udp.close()
        


