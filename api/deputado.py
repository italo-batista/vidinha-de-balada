# coding: utf-8

class Deputado:
	def __init__(self, ide, nome, alimentacao, combustivel, locacao, passagem, escritorio, divulgacao):

		self.id = ide
		self.valores = {

					"Nome" : nome,
					"Alimentação" : float(alimentacao),
					"Combustível" : float(combustivel),
					"Locação de veículos" : float(locacao),
					"Passagens aéreas" : float(passagem),
					"Escritório" : float(escritorio),
					"Divulgação de atividade parlamentar" : float(divulgacao),
					"Total" : (float(alimentacao) + float(combustivel) + float(locacao) + float(passagem) + float(escritorio) + float(divulgacao))
		}


	def __str__(self):
		return "%s %s" %(self.nome, self.valores["total"])


