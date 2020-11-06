# 3AT

#MAKEBASE

Lembre de definir o token do google nos arquivos!!!

makebase.py:

Pega o json adquirido do site
Faz a leitura
Em seguida faz as 130 consultas para saber a latitude e longitude de cada ponto
Salva em um json

makebase2.py:

Lê o json da etapa anterior
Faz os calculos geométricos para saber a distância entre os dois pontos pra podermos validar se o ponto tá em recife
Faz a leitura também do identificador (bairro)
Salva os dados que precisamos em um json

makebase3.py:
Lê o json da etapa anterior
Calcula as distâncias e se a distância for menor que 3km ele faz a consulta na API do google pra saber a distância de carro gerando então as arestas
Salva as arestas

#WEB

Desenvolvida com o framework Nuxt

#MAIN

O arquivo main.py disponibiliza a API na porta 8081 e faz a leitura do mapeamento.json e do database2.json para prover os dados e os calculos nas rotas:

ENDPOINT: /options (GET)
ENDPOINT: /calculate (POST)
  JSON:
  {
    "origin": 1,
    "destination": 12
  }
