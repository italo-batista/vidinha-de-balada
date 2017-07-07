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
grunt server
```

O navegador padrão abrirá automaticamente em [localhost:9000](http://localhost:9000).
