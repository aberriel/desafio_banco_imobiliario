# O Desafio

Considere o seguinte jogo hipotético muito semelhante a Banco Imobiliário, onde várias de suas mecânicas
foram simplificadas. Numa partida desse jogo, os jogadores se alteram em rodadas, numa ordem definida
aleatoriamente no começo da partida. Os jogadores sempre começam uma partida com saldo de 300 para
cada um.


Nesse jogo, o tabuleiro é composto por 20 propriedades em sequência. Cada propriedade tem um custo de
venda, um valor de aluguel, um proprietário caso já estejam compradas, e seguem uma determinada ordem no
tabuleiro. Não é possível construir hotéis e nenhuma outra melhoria sobre as propriedades do tabuleiro, por
simplicidade do problema.


No começo da sua vez, o jogador joga um dado equiprovável de 6 faces que determina quantas espaços no
tabuleiro o jogador vai andar.


- Ao cair em uma propriedade sem proprietário, o jogador pode escolher entre comprar ou não a
propriedade. Esse é a única forma pela qual uma propriedade pode ser comprada.
- Ao cair em uma propriedade que tem proprietário, ele deve pagar ao proprietário o valor do aluguel da
propriedade.
- Ao completar uma volta no tabuleiro, o jogador ganha 100 de saldo.


Jogadores só podem comprar propriedades caso ela não tenha dono e o jogador tenha o dinheiro da venda.
Ao comprar uma propriedade, o jogador perde o dinheiro e ganha a posse da propriedade.


Cada um dos jogadores tem uma implementação de comportamento diferente, que dita as ações que eles
vão tomar ao longo do jogo. Mais detalhes sobre o comportamento serão explicados mais à frente.


Um jogador que fica com saldo negativo perde o jogo, e não joga mais. Perde suas propriedades e portanto
podem ser compradas por qualquer outro jogador.


Termina quando restar somente um jogador com saldo positivo, a qualquer momento da partida. Esse jogador
é declarado o vencedor.


Desejamos rodar uma simulação para decidir qual a melhor estratégia. Para isso, idealizamos uma partida
com 4 diferentes tipos de possíveis jogadores. Os comportamentos definidos são:


- O jogador um é impulsivo;
- O jogador dois é exigente;
- O jogador três é cauteloso;
- O jogador quatro é aleatório;

O jogador *impulsivo* compra qualquer propriedade sobre a qual ele parar.


O jogador *exigente* compra qualquer propriedade, desde que o valor do aluguel dela seja maior do que 50.


O jogador *cauteloso* compra qualquer propriedade desde que ele tenha uma reserva de 80 saldo sobrando
depois de realizada a compra.


O jogador *aleatório* compra a propriedade que ele parar em cima com probabilidade de 50%.


Caso o jogo demore muito, como é de costume em jogos dessa natureza, o jogo termina na milésima rodada
com a vitória do jogador com mais saldo. O critério de desempate é a ordem de turno dos jogadores nesta
partida.


## Saída


Uma execução do programa proposto deve rodar 300 simulações, imprimindo no console os dados referentes
às execuções. Esperamos encontrar nos dados as seguintes informações:


> - Quantas partidas terminam por *time out* (1000 rodadas);
> - Quantos turnos em média demora uma partida;
> - Qual a porcentagem de vitórias por comportamento dos jogadores;
> - Qual o comportamento que mais vence.


# Implementação

O projeto consiste na implementação do jogo descrito no desafio e o algorítmo responsável por realizar
múltiplas execuções do mesmo em simulação e a análise dos dados coletados.

## Descrição do conteúdo da pasta

- src: contêm os arquivos-fonte da solução implementada e da realização da simulação, com geração dos
dados para impressão no terminal
- tests: contêm os testes unitários desenvolvidos para validar a implementação feita
- requirements.txt: arquivo contendo as dependências para execução da simulação
- tests.sh: script para execução dos testes

## Configurando o ambiente para a realização da simulação

Em um terminal, execute o seguinte:

```
$virtualenv -p python3.8 virtualenv/
$source virtualenv/bin/activate
$pip install -r requirements.txt
```

## Execução

Para executar a simulação, basta rodar os comando (com a virtualenv ativada):

```
$cd src/
$python -m main
```

## Execução pelo PyCharm

1. Atente para a área à esquerda, onde se localiza o navegador por arquivos. Abra o ítem "src", onde estão os arquivos-fonte
<img width="1440" alt="Captura de Tela 2021-11-22 às 13 02 20" src="https://user-images.githubusercontent.com/901052/142894553-ed230102-3cf6-4ee3-9663-6628a54d40e0.png">

2. Clique com o botão direito do mouse sobre o arquivo main.py. A opção "RUN 'main'" deve ser localizada e selecionada.
<img width="1440" alt="Captura de Tela 2021-11-22 às 13 03 06" src="https://user-images.githubusercontent.com/901052/142894623-c9db21b0-4c5b-47ae-a979-fcab28d8cdb0.png">

3. A execução aparecerá em uma área de terminal na parte de baixo do PyCharm, conforme pode ser visto abaixo.
<img width="1440" alt="Captura de Tela 2021-11-22 às 13 03 32" src="https://user-images.githubusercontent.com/901052/142894727-cc32c0f8-3811-4107-9813-6eeb041f0601.png">





## Testes

Como o tempo foi curto, ainda não consegui cobrir tudo com testes, mas alguns estão disponíveis
e podem ser executados a partir da pasta raiz do projeto (a que contem a "tests"e a "src"),
executando o seguinte comando:

```
$python -m pytest $(CAPTURE) --cov=tests --cov=src -W ignore::DeprecationWarning --cov-report term-missing:skip-covered
```
    
