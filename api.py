# coding: utf-8
import json
from flask import Flask, request
import sys
from gasto import *
from deputado import *
from collections import OrderedDict
import unicodedata
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


reload(sys)
sys.setdefaultencoding('utf8')

#colunas CSV
txNomeParlamentar = 0
idecadastro	 = 1
sgUF = 2 
ano = 3
mes = 4 
nossas_categorias = 5
codNossas_categorias = 6
total = 7
cota_mensal = 8
coef = 9

categorias_gastos = {}
ids_gastos = {}
categorias = set()
ids = set()
gastos_dict = {}

# def force_decode(string, codecs=['utf8', 'cp1252']):
#     for i in codecs:
#         try:
#             return string.decode(i)
#         except:
#             pass


f = open('data/gasto_mensal_por_depoutado_por_categoria.csv')
f.readline()

#line = [x.decode('utf8') for x in line]
for line in f:
    gasto = line.split(',')

    # cate = str(gasto[nossas_categorias])
    # cate = force_decode(str(cate))

    # cate = str(unicodedata.normalize('NFKD', cate).encode('utf-8','ignore'))

	# inclui gasto no dict de gastos
    gasto_obj = Gasto(gasto[txNomeParlamentar], gasto[idecadastro], gasto[sgUF], gasto[ano], gasto[mes], gasto[nossas_categorias], gasto[codNossas_categorias], gasto[total], gasto[cota_mensal], gasto[coef])

    # conjunto único de categorias
    categorias.add(gasto[nossas_categorias])

    #conjunto único de ids
    ids.add(gasto[idecadastro])

    gastos_dict[gasto_obj.idecadastro] = gasto_obj

    # constrói dict mapeando categoria para gastos
    # deve ser usado para melhorar o desempenho das buscas
    if gasto_obj.nossas_categorias in categorias_gastos:
        categorias_gastos[gasto_obj.nossas_categorias].append(gasto_obj)
    else:
        categorias_gastos[gasto_obj.nossas_categorias] = [gasto_obj]

    # constrói dict mapeando ids para gastos
    # deve ser usado para melhorar o desempenho das buscas
    if gasto_obj.idecadastro in ids_gastos:
        ids_gastos[gasto_obj.idecadastro].append(gasto_obj)
    else:
        ids_gastos[gasto_obj.idecadastro] = [gasto_obj]

# para trabalhar melhor com json
categorias = list(categorias)
ids = list(ids)

f.close()


@app.route('/')
def index():
    return "API no ar."

@app.route('/search')
def buscaCategoria():
    categorias_tag = request.args.get('categorias', [])
    keys = request.args.get('categoria').lower()
    keys = remover_combinantes(keys).split()
    categorias_key = categorias
    if categorias_tag:
        categorias_key = categorias_tag.encode('utf-8').split(',')

    collection = apply_filtro(gastos_dict.values, categorias_key)
    out = []

    for gasto in collection:
    	if keys[0] in str(gasto.nossas_categorias).lower():
            matches = {
                'txNomeParlamentar' : gasto.txNomeParlamentar,
                'idecadastro' : gasto.idecadastro,
                'sgUF' : gasto.sgUF,
                'ano' : gasto.ano,
                'mes' : gasto.mes,
                'nossas_categorias' : gasto.nossas_categorias,
                'codNossas_categorias' : gasto.codNossas_categorias,
                'total' : gasto.total,
                'cota_mensal' : gasto.cota_mensal,
                'coef' : gasto.coef,

            }
            out.append(matches)
    return json.dumps(out)

@app.route('/gasto')
def buscaid():
    ids_tag = request.args.get('nome', [])
    keys = request.args.get('id').lower()
    keys = remover_combinantes(keys).split()

    ids_key = ids
    if ids_tag:
        ids_key = ids_tag.encode('utf-8').split(',')

    collection = apply_filtro_nome(gastos_dict.values, ids_key)
    out = []

    for gasto in collection:
    	if keys[0] in str(gasto.idecadastro):
            matches = {
                'txNomeParlamentar' : gasto.txNomeParlamentar,
                'idecadastro' : gasto.idecadastro,
                'sgUF' : gasto.sgUF,
                'ano' : gasto.ano,
                'mes' : gasto.mes,
                'nossas_categorias' : gasto.nossas_categorias,
                'codNossas_categorias' : gasto.codNossas_categorias,
                'total' : gasto.total,
                'cota_mensal' : gasto.cota_mensal,
                'coef' : gasto.coef,

            }
            out.append(matches)
    return json.dumps(out)


## Filtra a coleção de gastos por categoria.
def apply_filtro(gastos, categorias_key):
    # filtra para melhor desempenho
    collection = []
    for categoria in categorias_key:
        if categoria in categorias:
            collection += categorias_gastos[categoria]
    return collection

## Filtra a coleção de gastos por ca\tegoria.
def apply_filtro_nome(gastos, ids_key):
    # filtra para melhor desempenho
    collection = []
    for nome in ids_key:
        if nome in ids:
            collection += ids_gastos[nome]
    return collection


def remover_combinantes(string):
    string = unicodedata.normalize('NFD', string)
    return u''.join(ch for ch in string if unicodedata.category(ch) != 'Mn')



deputados_dict = {}

f = open('data/tabela_gastos_por_categoria.csv')
f.readline()


for line in f:
	deputado = line.split(",")

	dep_obj = Deputado(deputado[0], deputado[1], deputado[2], deputado[3], deputado[4], deputado[5], deputado[6], deputado[7])

	deputados_dict[deputado[0]] = dep_obj.valores

f.close()

ranking = []
f = open('data/top_10_estourados_brasil.csv')
f.readline()

for line in f:
	rank = line.split(",")
	valores = {  "nome" : rank[0],
				"id" : rank[1],
	             "uf" : rank[2],
				"ano" : int(rank[3]),
				"mes" : int(rank[4]),
				"total" : float(rank[5]),
				"cota_mensal" : float(rank[6]),
				"coef" : float(rank[7])
	}      
	ranking.append(valores)

f.close()

@app.route('/top10')
def top10():
	return json.dumps(ranking)

f = open('data/busca.csv')
f.readline()

for line in f:
	info = line.split(",")
	if info[0] in deputados_dict.keys():
		deputados_dict[info[0]]["urlfoto"] = info[2]
	for dep in ranking:
		if info[0] in dep["id"]:
			dep["urlfoto"] = info[2]


f.close()


@app.route('/todos')
def deputados():
	return json.dumps(deputados_dict)

@app.route('/deputado')
def deputado_por_id():
	key = request.args.get('id').lower()
	return json.dumps(deputados_dict[key])


gastos_anos = {}
f = open('data/gasto_total_anos.csv')
f.readline()

for line in f:
	gasto_anual = line.split(",")
	valores = [float(gasto_anual[1]), float(gasto_anual[2])]
	gastos_anos[gasto_anual[0]] = valores

f.close()


@app.route('/gasto_anual')
def anual():
	key =request.args.get('ano').lower()
	return json.dumps(gastos_anos[key])





f = open('data/total_presenca_anos_somados.csv')
f.readline()

for line in f:
	info = line.split(",")
	if info[0] in deputados_dict.keys():
		deputados_dict[info[0]]["presencas"] = int(info[2])
		deputados_dict[info[0]]["total_sessoes"] = int(info[3])
	for dep in ranking:
		if info[0] in dep["id"]:
			dep["presencas"] = int(info[2])
			dep["total_sessoes"] = int(info[3])


f.close()

if __name__ == '__main__':
    app.run(debug=True)

