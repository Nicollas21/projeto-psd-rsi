from Pacote import *

import sys


class Analise:
    
    def __init__(self):
        self.lista_pacotes = []

    #adiciona cada objeto do pacote na lista.
    def adicionar_lista(self, pacote):
        self.lista_pacotes.append(pacote)
    
    #calcula o total de aplicacoes que passaram na fila.
    def totalPacotes(self):
        total = 0
        for p in self.lista_pacotes:
            print p.getTipo()
            total += 1
        
        print "Total de Aplicacoes %d\n " % (total)
        
    #dados a respeito do protocolo Bittorrent.
    def dadosBittorrent(self):
        bittorrent_count = 0 
        bittorrent_tamanho = 0
        for p in self.lista_pacotes:
            if (p.getTipo() == "bittorrent"):
                bittorrent_count += 1
                bittorrent_tamanho += p.getTamanho()
        
        print (bittorrent_tamaho/bittorrent_count)
                
        
    #dados do protocolo DHCP.
    def dadosDhcp(self):
        total = 0
        dhcp_count = 0 
        dhcp_tamanho = 0
        for p in self.lista_pacotes:
            total += 1
            if (p.getTipo() == "ssdp"):
                dhcp_count += 1
                dhcp_tamanho += float(p.getTamanho())
        print "DHCP"
        print "Tamanho Medio dos Pacotes: %d " % float(dhcp_tamanho/ssl_count)
        print "Percentual da Aplicacao: %d " % ((dhcp_count/total)*100)  
    
            
    def dadosHttp(self):
        total = 0
        http_count = 0 
        http_tamanho = 0
        for p in self.lista_pacotes:
            total += 1
            if (p.getTipo() == "http"):
                http_count += 1
                http_tamanho += float(p.getTamanho())
        print "HTTP"
        print "Tamanho Medio dos Pacotes: %d " % float(http_tamanho/http_count)
        print "Percentual da Aplicacao: %d " %((http_count/total)*100)

    #dados do protocolo SSDP.
    def dadosSsdp(self):
        total = 0
        ssdp_count = 0 
        ssdp_tamanho = 0
        for p in self.lista_pacotes:
            total += 1
            if (p.getTipo() == "ssdp"):
                ssdp_count += 1
                ssdp_tamanho += float(p.getTamanho())
        print "SSDP"
        print "Tamanho Medio dos Pacotes: %d " % float(ssdp_tamanho/ssdp_count)
        print "Percentual da Aplicacao: %d " % ((ssdp_count/total)*100)  
   
    #dados do protocolo SSH.
    def dadosSsh(self):
        total = 0
        ssh_count = 0 
        ssh_tamanho = 0
        for p in self.lista_pacotes:
            total += 1
            if (p.getTipo() == "ssdp"):
                ssh_count += 1
                ssh_tamanho += float(p.getTamanho())
        print "SSH"
        print "Tamanho Medio dos Pacotes: %d " % float(ssh_tamanho/ssh_count)
        print "Percentual da Aplicacao: %d " % ((ssh_count/total)*100)  
    
    #dados do protocolo SSL.
    def dadosSsl(self):
        total = 0
        ssl_count = 0 
        ssl_tamanho = 0
        for p in self.lista_pacotes:
            total += 1
            if (p.getTipo() == "ssdp"):
                ssl_count += 1
                ssl_tamanho += float(p.getTamanho())
        print "SSL"
        print "Tamanho Medio dos Pacotes: %d " % float(ssl_tamanho/ssl_count)
        print "Percentual da Aplicacao: %d " % ((ssl_count/total)*100)  
    
    #dados dos pacotes desconhecidos.
    def dadosUnknown(self):
        total = 0
        unknown_count = 0 
        unknown_tamanho = 0
        for p in self.lista_pacotes:
            total += 1
            if (p.getTipo() == "ssdp"):
                unknown_count += 1
                unknown_tamanho += float(p.getTamanho())
        print "UNKNOWN"
        print "Tamanho Medio dos Pacotes: %d " % float(unknown_tamanho/unknown_count)
        print "Percentual da Aplicacao: %d " % ((unknown_count/total)*100)  
    
    