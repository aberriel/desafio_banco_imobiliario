from .player_base import Player
import numpy


class RandomPlayer(Player):
    def __init__(self, properties=None, house=0, balance=300, name='Aleatorio', order=0):
        super(RandomPlayer, self).__init__(
            name=name,
            house=house,
            properties=properties,
            balance=balance,
            order=order)

    def buy(self, property):
        can_buy = numpy.random.randint(low=0, high=2)
        if can_buy == 1:
            self.balance -= property.purchase_price
            if self.balance < 0:
                return False
            self.properties.append(property)
            property.owner = self
            self.player_info['buy_payments'].append(property.purchase_price)
        return True
