import os


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