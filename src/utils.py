import os


# Hack para resolver o problema dos imports que nunca funcionaram para os casos
# de execução normal (pelo PyCharm ou terminal direto).
if 'src' in os.getcwd():
    from player import (
        RandomPlayer,
        CautiousPlayer,
        DemandingPlayer,
        ImpulsivePlayer)
else:
    from src.player import (
        RandomPlayer,
        CautiousPlayer,
        DemandingPlayer,
        ImpulsivePlayer)
import random


def make_players_with_aleatory_order():
    '''
    Cria jogadores aleatórios (no caso, um de cada tipo) e os ordena por uma ordem aleatória.
    :return: Lista de jogadores criada em ordem aleatória
    '''
    player_1 = RandomPlayer()
    player_2 = CautiousPlayer()
    player_3 = DemandingPlayer()
    player_4 = ImpulsivePlayer()
    raw_players = [player_1, player_2, player_3, player_4]
    players = dict()

    order = random.sample(range(4), 4)
    player_counter = 0
    for order_item in order:
        raw_players[player_counter].order = order_item + 1
        players[order_item + 1] = raw_players[player_counter]
        player_counter += 1
    return players