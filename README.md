## [Vidinha de Balada](http://vidinhadebalada.com/#!/)

Você sabia que, além do salário, os deputados federais recebem outras verbas para exercer seus cargos? Dentre elas: auxílio para contratar funcionários, auxílio moradia, despesas com saúde, entre outras. No Vidinha de Balada, vamos falar em especial da CEAP (Cota para Exercício da Atividade Parlamentar). Para saber mais sobre a CEAP acesse [este link](http://vidinhadebalada.com).

Na plataforma você pode conferir:

- Valor gasto com a CEAP no atual mandato (e valores comparativos)
- Os TOP10 deputados reis do camarote mais gastadores do Brasil (e também por estado ou partido)
- Presença dos deputados nas sessões e gastos ao longo dos meses/anos
- Valor gasto por categoria (alimentação, locação de veículos, etc)

E várias outras informações do seu representante. Acesse o [Vidinha de Balada](http://vidinhadebalada.com/#!/) e acompanhe de perto o trabalho de quem você escolheu pra te representar!


O [Vidinha de Balada](http://vidinhadebalada.com/#!/) surgiu no [Hackfest Contra a Corrupção](http://hackfest.com.br/).


----

Deseja contribuir com o Vidinha de Balada?! Melhorias são muito bem-vindas! :))


### Requisitos

Este projeto é dividido em duas partes, _frontend_ e _backend_ e necessita da instalação prévia dos seguintes requisitos:

- Python >= 2.7.2, <3.0
- pip >= 6.1
- NodeJS >= 4.0
- Grunt-cli >= 1.2
- Bower >= 1.8
- Mysql >= 5.7.19
- R version >= 3.4.0

### Desenvolvimento

- Para rodar o **frontend** em modo de desenvolvimento, entre no diretório _web_ do projeto e use os comandos:

Para instalar as dependências:
```
cd web
npm install
bower install
```
Para rodar:
```
grunt serve
```

O navegador padrão abrirá automaticamente em [localhost:9000](http://localhost:9000).


- Para rodar o **backend**, existem 2 opções: utilizar nosso banco de dados e API rest (configurados e disponíveis), ou montar sua própria infraestrutura localmente.

Para a primeira opção, basta clonar o projeto e se divertir! :D

Para a segunda opção é necessário i) gerar os arquivos de dados, ii) popular o banco de dados e iii) levantar a APIrest.  

i) Para gerar os arquivos necessários, utilizando o R, execute o arquivo **/script/gera_csvs.R**

Após instalado o MySQL, execute o seguinte comando para gerar o esquema relacional do BD :

```
> source /~path_local/vidinha-de-balada/script/banco/vidinha-banco.sql
```

ii) Preenchimento do banco de dados com os arquivos gerados (é necessário editar este script e adicionar seu path ):

```
> source /~path_local/vidinha-de-balada/script/banco/populabanco.sql.
```

iii) Estando no diretório raiz do projeto, use os comandos:

Para instalar as dependências da API:
```
  pip install -r requirements.txt
```
Para rodar a API:
```
  python app.py
```

### Deployment

## Backend

Para o deploy do backend é necessário repetir os passos de montagem e preenchimento do banco e levantamento da API no servidor desejado.

## Frontend

Para realizar o deployment do frontend, é preciso gerar os arquivos próprios para serem servidos em produção,
isto é, arquivos HTML, CSS e Javascript concatenados, minificados e otimizados. Antes de tudo, copie e modifique
o arquivo _secret.json.example_ para _secret.json_ e preencha-o com os dados de acordo com a sua realidade.
Nunca submeta o arquivo _secret.json_ no versionamento do GIT pois ele contem informações do servidor (como usuário e senha).

Para gerar os arquivos de produção:
```
grunt build
```

Isso criará o diretório _dist/_ que deve ser enviado para o servidor de produção:

Para enviar os arquivos para o servidor:
```
grunt ssh_deploy:prod
```

Este comando utiliza o arquivo _secret.json_ para enviar os arquivos em _dist/_ para o servidor via SSH.

