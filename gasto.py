class Gasto:



	def __init__(self, txNomeParlamentar, idecadastro, sgUF, ano, mes, nossas_categorias, codNossas_categorias, total, cota_mensal, coef):

		self.txNomeParlamentar = txNomeParlamentar

		self.idecadastro = idecadastro
		self.sgUF = sgUF
		self.ano = ano
		self.mes = mes
		self.nossas_categorias = nossas_categorias
		self.codNossas_categorias = codNossas_categorias
		self.total = total
		self.cota_mensal = cota_mensal
		self.coef = coef



    #def __str__(self):
    #    return '%s,%s,%s' % (self.txNomeParlamentar, self.sgUF, self.total)