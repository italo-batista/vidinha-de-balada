## [Vidinha de Balada](https://italo-batista.github.io/vidinha-de-balada/#!/)

Vidinha de Balada surgiu no [Hackfest Contra a Corrupção](http://hackfest.com.br/).

O projeto propõe analisar os gastos da CEAP (Cota para o Exercício da Atividade Parlamentar), possibilitando ao cidadão comum:

- verificar se o gasto do deputado é proporcional a sua presença e/ou participação nas sessões da câmara;
- comparar facilmente os valores gastos pelos deputados com parâmetros conhecidos.

Com os gestores (deputados) em foco, é possível acompanhar:

- Gastômetro (o que foi gastado com a CEAP no presente ano);
- Top deputados gastadores;
- Presença nas sessões e gastos ao longo dos meses;
- Gastos por categoria;
- Timeline de presenças e gastos.

----

O projeto está em fase de desenvolvimento. Melhorias são muito bem-vindas! :))

### Requisitos

Este projeto é dividido em duas partes, _frontend_ e _backend_ e necessita da instalação prévia dos seguintes requisitos:

- Python >= 2.7.2, <3.0
- pip >= 6.1
- NodeJS >= 4.0
- Grunt-cli >= 1.2
- Bower >= 1.8

### Desenvolvimento

Para rodar o backend, estando no diretório raiz do projeto, use os comandos:

Para instalar as dependências:
```
  pip install -r requirements.txt
```
Para rodar:
```
  python app.py
```

Para rodar o frontend em modo de desenvolvimento, entre no diretório _web_ do projeto e use os comandos:

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

### Deployment

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
