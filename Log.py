from datetime import datetime
import os.path

class Logs():
        nome_arq = ""
	def setError(self,mensagem,coletor):
		today = datetime.now()
		self.nome_arq = "logs_"+coletor+".txt"
		arquivo = open(self.nome_arq,"a+")
		arquivo.write(str(today)+" - "+str(mensagem)+"\n")
		arquivo.close

	def getError(self):
		if os.path.isfile(self.nome_arq):
			arquivo = open(self.nome_arq,"r")
			mensagem = arquivo.read()
			arquivo.close
			return mensagem
		else:
			return "arquivo nao encontrado"
