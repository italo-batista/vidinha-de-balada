## [Vidinha de Balada](http://vidinhadebalada.com/#!/)

### Objetivos 

A proposta do Vidinha de Balada é simplificar os dados públicos (gastos e presenças nas sessões) ao ponto de que o cidadão comum possa entender, falando sobre os gastos dos deputados em termos de salários mínimos, casas populares, cestas básica - tudo isso de forma bem humorada.


### Potencial do Vidinha de Balada

Acreditamos que o potencial do Vidinha de Balada está atrelado ao jeito lúdico de lidar com um tema tão importante, ainda pouco explorado e, de certa forma, inacessível à grande parcela dos brasileiros  - os gastos dos seus representantes. 
Para facilitar o entendimento desses valores gastos, os colocamos em termos entendíveis pelo cidadão comum: comparando com quantidade de salários mínimos, de casas populares que poderiam ser construídas, entre outros. Para cada uso excedido da cota em uma determinada categoria, o deputado receberá selos como por exemplo “top gastador com passagens aéreas” ou “top gastador comilão”.

Acreditamos que nosso projeto possui grande potencial de impacto principalmente entre a parcela mais leiga (em relação a dados/gastos públicos) da população, pela facilidade no entendimento da utilização do dinheiro que sai do bolso do contribuinte.


### Design e Usabilidade

A partir do nome do projeto, buscamos trazer para o ambiente da aplicação elementos que remetessem a uma balada (festa), como por exemplo: as cores identificadas em jogos de luzes de casas noturnas, linguagem descontraída e comparações com elementos do cotidiano de um trabalhador brasileiro, como por exemplo salário mínimo.

Após entendermos os dados fornecidos pela câmara, definimos quais informações seriam apresentadas ao usuário. Hierarquizamos informações e as subdividimos em áreas, para que o usuário ao visitar as páginas identificasse as sessões de seu interesse.

### Infraestrutura

A infraestrutura necessária para manutenção do Vidinha de Balada é composta de:

- Servidor linux (r +pacotes, python, git, apache)
- Domínio pago anualmente (vidinhadebalada.com - )

Caso o projeto seja hospedado por algum órgão (MP, CGU, etc), estes custos não existiriam.


### Sustentabilidade

Em relação a facilidade obtenção dos dados: 

- Os dados de gastos utilizados na plataforma são baixados automaticamente através do script gera_csvs.R (/script/gera_csvs.R) - atualização mensal dos gastos é feita automaticamente. 
- Os dados de presença são provenientes das sessões de votação realizadas na câmara.

Entretanto a Câmara lançou recentemente uma API aberta com os dados da câmara (https://dadosabertos.camara.leg.br/) e é possível, num futuro próximo, que todos os dados que utilizamos sejam provenientes desta. Para a entrega da Segunda Fase do Hackfest optamos por montar nossa própria estrutura por temer que o serviço da Cãmara (ainda em fase de testes) saísse do ar.

Especificidades e modificações:

- Atualmente a plataforma está construída para o mandato 2015-2018. Seriam necessárias algumas modificações para navegar entre mandatos.











