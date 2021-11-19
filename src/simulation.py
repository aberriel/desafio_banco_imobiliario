from .house import House
from .config import Config
from .game import Game
from .property import Property
from .utils import *
import time


class Simulation:
    def __init__(self):
        self.players = make_players_with_aleatory_order()
        self.houses = self.make_houses()

    def make_houses(self):
        config = Config()
        houses = dict()
        counter = 0
        while counter <= max(config.properties.keys()):
            house = House(position=0)
            if counter > 0:
                raw_property = config.properties[counter]
                property = Property(
                    purchase_price=raw_property['purchase_price'],
                    rent_amount=raw_property['rent_amount'],
                    name=raw_property['name'] if 'name' in raw_property else '',
                    house=counter)
                house.property = property
            houses[counter] = house
            counter += 1
        return houses

    def run(self):
        self.game = Game(players=self.players, houses=self.houses)

        start = time.time()
        while True:
            self.game.next_play()
            if self.game.round >= 1000 or self.game.has_winner() is not None:
                break
        end = time.time()

        result = {
            'total_time': end - start,
            'total_rounds': self.game.round,
            'last_player': self.game.actual_player}

        winner = self.game.has_winner()
        result['winner'] = winner.name if winner is not None else None
        result['winner_final_balance'] = winner.balance if winner else 0
        return result
