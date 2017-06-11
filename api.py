# coding: utf-8
import json
from flask import Flask, request
import sys
from gasto import *
from collections import OrderedDict
import unicodedata

app = Flask(__name__)

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
nomes_gastos = {}
categorias = set()
nomes = set()
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

    #conjunto único de nomes
    nomes.add(gasto[txNomeParlamentar])

    gastos_dict[gasto_obj.idecadastro] = gasto_obj

    # constrói dict mapeando categoria para gastos
    # deve ser usado para melhorar o desempenho das buscas
    if gasto_obj.nossas_categorias in categorias_gastos:
        categorias_gastos[gasto_obj.nossas_categorias].append(gasto_obj)
    else:
        categorias_gastos[gasto_obj.nossas_categorias] = [gasto_obj]

    # constrói dict mapeando Nomes para gastos
    # deve ser usado para melhorar o desempenho das buscas
    if gasto_obj.txNomeParlamentar in nomes_gastos:
        nomes_gastos[gasto_obj.txNomeParlamentar].append(gasto_obj)
    else:
        nomes_gastos[gasto_obj.txNomeParlamentar] = [gasto_obj]

# para trabalhar melhor com json
categorias = list(categorias)
nomes = list(nomes)

f.close()


@app.route('/')
def index():
    return "API no ar."

@app.route('/searchCategory')
def buscaCategoria():
    categorias_tag = request.args.get('categorias', [])
    keys = request.args.get('key').lower()
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

@app.route('/searchName')
def buscaNome():
    nomes_tag = request.args.get('nome', [])
    keys = request.args.get('key').lower()
    keys = remover_combinantes(keys).split()

    nomes_key = nomes
    if nomes_tag:
        nomes_key = nomes_tag.encode('utf-8').split(',')

    collection = apply_filtro_nome(gastos_dict.values, nomes_key)
    out = []

    for gasto in collection:
    	if keys[0] in str(gasto.txNomeParlamentar).lower():
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

## Filtra a coleção de gastos por categoria.
def apply_filtro_nome(gastos, nomes_key):
    # filtra para melhor desempenho
    collection = []
    for nome in nomes_key:
        if nome in nomes:
            collection += nomes_gastos[nome]
    return collection


def remover_combinantes(string):
    string = unicodedata.normalize('NFD', string)
    return u''.join(ch for ch in string if unicodedata.category(ch) != 'Mn')

if __name__ == '__main__':
    app.run(debug=True)

