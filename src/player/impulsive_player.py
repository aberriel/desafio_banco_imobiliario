from .player_base import Player


class ImpulsivePlayer(Player):
    def __init__(self, properties=None, house=0, balance=300, name='Impulsive', order=0):
        super(ImpulsivePlayer, self).__init__(
            name=name,
            house=house,
            properties=properties,
            balance=balance,
            order=order)

    def buy(self, property):
        self.balance -= property.purchase_price
        if self.balance < 0:
            return False
        self.properties.append(property)
        property.owner = self
        self.player_info['buy_payments'].append(property.purchase_price)
        return True
