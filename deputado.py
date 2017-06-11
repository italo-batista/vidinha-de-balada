class Deputado:
	def __init__(self, ide, nome, alimentacao, combustivel, locacao, passagem, escritorio, divulgacao):

		self.id = ide
		self.valores = {
					"nome" : nome,
					"alimentacao" : float(alimentacao),
					"combustivel" : float(combustivel),
					"locacao" : float(locacao),
					"passagem" : float(passagem),
					"escritorio" : float(escritorio),
					"divulgacao" : float(divulgacao),
					"total" : (float(alimentacao) + float(combustivel) + float(locacao) + float(passagem) + float(escritorio) + float(divulgacao))
		}


	def __str__(self):
		return "%s %s" %(self.nome, self.valores["total"])


