
class Pacote:
	
	def __init__(self, tipo, tamanho, tempo):
		self.tipo = tipo
		self.tamanho = tamanho
		self.tempo = tempo
		
	def getTamanho(self):
		return self.tamanho
	
	def getTipo(self):
		return self.tipo
		
	def getTempo(self):
		return self.tempo
		
	def imprimir(self):
		print "Aplicacao: %r\n Tamanho: %d\n Tempo: %d\n " % (self.getTipo(), self.getTamanho(), self.getTempo())