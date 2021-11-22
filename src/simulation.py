import os


if 'src' in os.getcwd():
    from config import Config
    from game import Game
    from house import House
    from property import Property
    from utils import *
else:
    from src.config import Config
    from src.game import Game
    from src.house import House
    from src.property import Property
    from src.utils import *
import time


class Simulation:
    game = None
    game_config = None

    def __init__(self, game_config=None):
        self.players = make_players_with_aleatory_order()
        self.houses = self.make_houses()
        self.game_config = game_config

    def make_houses(self):
        if not self.game_config:
            config = Config()
            self.game_config = config.properties_2

        houses = dict()
        counter = 0
        while counter <= max(self.game_config.keys()):
            house = House(position=0)
            if counter > 0:
                raw_property = self.game_config[counter]
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
            'total_rounds': self.game.round}

        winner = self.game.has_winner()
        result['status'] = 'finished_by_winner' if winner is not None else 'finished_by_timeout'

        result['winner'] = winner.name if winner is not None else None
        result['winner_final_balance'] = float(winner.balance) if winner else 0
        result['players_info'] = self.game.players_report_info
        return result
