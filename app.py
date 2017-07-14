#!/usr/bin/python
# coding: utf-8
import json
from flask import Flask, request, make_response, Response
import os
import sys
sys.path.insert(0, 'api')
from gasto import *
from deputado import *
from collections import OrderedDict
import unicodedata
from flask_cors import CORS, cross_origin
import csv

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




def force_decode(string, codecs=['utf8', 'cp1252']):
    for i in codecs:
        try:
            return string.decode(i)
        except:
            pass

@app.route('/teste')
def todos_deputados():
    lista_deputados = []
    with open('data/gerados-hackfest/gasto_mensal_por_depoutado_por_categoria.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            info_deputado = {}
            id_deputado = str(unicodedata.normalize('NFKD', force_decode(row['idecadastro'])).encode('utf-8','ignore'))
            nome_deputado = str(unicodedata.normalize('NFKD', force_decode(row['txNomeParlamentar'])).encode('utf-8','ignore'))
            categoria = str(unicodedata.normalize('NFKD', force_decode(row['nossas_categorias'])).encode('utf-8','ignore'))
            estado = str(unicodedata.normalize('NFKD', force_decode(row['sgUF'])).encode('utf-8','ignore'))
            info_deputado = {
                "txNomeParlamentar" : nome_deputado,
                "idecadastro" : id_deputado,
                "sgUF" : estado,
                "ano" : int(row['ano']),
                "mes" : int(row['mes']),
                "nossas_categorias" : categoria,
                "codNossas_categorias" : int(row['codNossas_categorias']),
                "total" : float(row['total']),
                "cota_mensal" : float(row['cota_mensal']),
                "coef" : float(row['coef'])

                }
            lista_deputados.append(info_deputado)
    return json.dumps(lista_deputados, ensure_ascii=False).encode('utf-8')



lista_deputados = []
with open('data/gerados-hackfest/gasto_mensal_por_depoutado_por_categoria.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=",")
    for row in reader:
        info_deputado = {}
        id_deputado = str(unicodedata.normalize('NFKD', force_decode(row['idecadastro'])).encode('utf-8','ignore'))
        nome_deputado = str(unicodedata.normalize('NFKD', force_decode(row['txNomeParlamentar'])).encode('utf-8','ignore'))
        categoria = str(unicodedata.normalize('NFKD', force_decode(row['nossas_categorias'])).encode('utf-8','ignore'))
        estado = str(unicodedata.normalize('NFKD', force_decode(row['sgUF'])).encode('utf-8','ignore'))

        gasto_obj = Gasto(nome_deputado,
            id_deputado,
            estado,
            int(row['ano']),
            int(row['mes']),
            categoria,
            int(row['codNossas_categorias']),
            float(row['total']),
            float(row['cota_mensal']),
            float(row['coef']) )

        # conjunto único de categorias
        categorias.add(categoria)

        #conjunto único de ids
        ids.add(id_deputado)

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


@app.route('/')
def index():
    return "API no ar."

@app.route('/search')
def buscaCategoria():
    categorias_tag = request.args.get('categorias', [])
    keys = request.args.get('categoria').lower()
    keys = normalizar_codificacao(keys).split()
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


    response = make_response(json.dumps(out, ensure_ascii=False).encode('utf-8'))
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

@app.route('/gasto')
def buscaid():
    ids_tag = request.args.get('nome', [])
    keys = request.args.get('id').lower()
    keys = normalizar_codificacao(keys).split()

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
    return json.dumps(out, ensure_ascii=False).encode('utf-8')


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


def normalizar_codificacao(string):
    string = str(unicodedata.normalize('NFKD', force_decode(string)).encode('utf-8','ignore'))
    return string



deputados_dict = {}

# f = open('data/gerados-hackfest/tabela_gastos_por_categoria.csv')
# f.readline()


# for line in f:
#     deputado = line.split(",")
#     id_deputado = str(unicodedata.normalize('NFKD', force_decode(deputado[0])).encode('utf-8','ignore'))
#     nome_deputado = str(unicodedata.normalize('NFKD', force_decode(deputado[1])).encode('utf-8','ignore'))
#     dep_obj = Deputado(id_deputado, nome_deputado, deputado[2], deputado[3], deputado[4], deputado[5], deputado[6], deputado[7])

#     deputados_dict[deputado[0]] = dep_obj.valores

# f.close()

with open('data/gerados-hackfest/tabela_gastos_por_categoria.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=",")
    for row in reader:
        nome_deputado = str(unicodedata.normalize('NFKD', force_decode(row['txNomeParlamentar'])).encode('utf-8','ignore'))

        dep_obj = Deputado(row['idecadastro'],
            nome_deputado,
            row['Alimentação'],
            row['Combustível'],
            row['Locação de veículos'],
            row['Passagens aéreas'],
            row['Escritório'],
            row['Divulgação de atividade parlamentar'])

        deputados_dict[row['idecadastro']] = dep_obj.valores



ranking = []

with open('data/gerados-hackfest/top_10_estourados_brasil.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=",")
    for row in reader:
        nome_deputado = str(unicodedata.normalize('NFKD', force_decode(row['txNomeParlamentar'])).encode('utf-8','ignore'))
        valores = {  "nome" : nome_deputado,
                "id" : row['idecadastro'],
                 "uf" : row['sgUF'],
                "ano" : int(row['ano']),
                "mes" : int(row['mes']),
                "total" : float(row['total']),
                "cota_mensal" : float(row['cota_mensal']),
                "coef" : float(row['coef'])
        }
        ranking.append(valores)


@app.route('/top10')
def top10():
	return json.dumps(ranking, ensure_ascii=False).encode('utf-8'  )


with open('data/gerados-hackfest/busca.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=",")
    for row in reader:
        id_deputado = row['idecadastro']
        urlfoto = str(unicodedata.normalize('NFKD', force_decode(row['urlFoto'])).encode('utf-8','ignore'))
        if id_deputado in deputados_dict.keys():
            deputados_dict[id_deputado]["urlfoto"] = urlfoto
        for dep in ranking:
            if id_deputado in dep["id"]:
                dep["urlfoto"] = urlfoto

@app.route('/todos')
def deputados():
	return json.dumps(deputados_dict,  ensure_ascii=False).encode('utf-8')

#busca deputado a partir do seu ID
#/deputado?id=
@app.route('/deputado')
def deputado_por_id():
	key = request.args.get('id').lower()
	return json.dumps(deputados_dict[key], ensure_ascii=False).encode('utf-8')


gastos_anos = {}
f = open('data/gerados-hackfest/gasto_total_anos.csv')
f.readline()

for line in f:
	gasto_anual = line.split(",")
	valores = [float(gasto_anual[1]), float(gasto_anual[2])]
	gastos_anos[gasto_anual[0]] = valores

f.close()


#/gasto_anual?ano=
@app.route('/gasto_anual')
def anual():
	key =request.args.get('ano').lower()
	return json.dumps(gastos_anos[key], ensure_ascii=False).encode('utf-8')

f = open('data/gerados-hackfest/total_presenca_anos_somados.csv')
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

@app.route("/busca")
def busca_deputado_por_nome():
    nome = request.args.get('nome').lower()
    resultados = []
    deputado = {}
    for key,value in deputados_dict.iteritems():
        if nome in value['Nome'].lower():
            deputado['nome'] = value['Nome']
            deputado['id'] = key
            resultados.append(deputado)
            deputado = {}
    return json.dumps(resultados, ensure_ascii=False).encode('utf-8')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
