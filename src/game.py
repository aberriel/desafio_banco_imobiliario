from .house import House
from .jogador import (
    RandomPlayer,
    CautiousPlayer,
    DemandingPlayer,
    ImpulsivePlayer)
from .property import Property
from .utils import *
import numpy
import random


class Game:
    game_report = dict()

    def __init__(self, round=0, players=None, houses=None, actual_player=1):
        self.round = round
        self.players = players or dict()
        self.houses = houses or dict()
        self.actual_player = actual_player or 1

        if len(self.players.keys()) == 0:
            self.players = make_players_with_aleatory_order()

        if len(self.houses.keys()) == 0:
            self.make_random_houses()

        self.arrange_players_houses()

    def _prepare_report(self):
        self.game_report = {
            'players': {}
        }

        for pointer in self.players.keys():
            self.game_report['players'][pointer] = {
                'name': self.players[pointer]['name'],
                'order': pointer
            }

    def make_random_houses(self):
        counter = 0
        while counter <= 20:
            house = House(position=counter)
            if counter > 0:
                purchase_price = numpy.random.randint(low=2, high=301)
                rent_amount = numpy.random.randint(low=0, high=purchase_price/2)
                if rent_amount == 0:
                    rent_amount = 1
                property = Property(
                    purchase_price=purchase_price,
                    rent_amount=rent_amount,
                    name=f'Casa {counter}')
                house.property = property
            self.houses[counter] = house
            counter += 1

    def arrange_players_houses(self):
        for player_position in self.players.keys():
            self.houses[0].players.append(self.players[player_position])
            self.players[player_position].house = 0

    def get_next_player(self):
        next = self.actual_player + 1
        if next > len(self.players.keys()):
            next = 1
        return next

    def remove_player(self, jogador):
        self.houses[jogador.house].players.remove(jogador)
        del self.players[jogador.ordem]

        # Agora vamos reestruturar os players
        counter = 1
        dict_players_2 = dict()
        for item in self.players.keys():
            dict_players_2[counter] = self.players[item]
            dict_players_2[counter].ordem = counter
            counter += 1
        self.players  =dict_players_2

    def update_player_house(self, jogador, casa_final):
        self.houses[jogador.house].players.remove(jogador)
        jogador.house = casa_final
        self.houses[casa_final].players.append(jogador)

    def next_play(self):
        player = self.players[self.actual_player]
        dice = numpy.random.randint(low=1, high=7)
        next_house = player.get_next_house(dice, len(self.houses.keys()) - 1)
        self.update_player_house(player, next_house)

        if self.houses[next_house].property is not None:
            operation_result = player.buy_or_rent(self.houses[next_house].property)
            if not operation_result:
                print(f'Player.next_play -> Jogador {player.name} rodando na rodada {self.round}')
                player.lose_all()
                self.remove_player(player)

        self.actual_player = self.get_next_player()
        self.round += 1

    def has_winner(self):
        if len(self.players.keys()) == 1:
            return self.players[1]
        return None
