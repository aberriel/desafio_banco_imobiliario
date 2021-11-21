from .player_base import Player


class CautiousPlayer(Player):
    def __init__(self, properties=None, house=0, balance=300, name='Cautelous', order=0):
        super(CautiousPlayer, self).__init__(
            name=name,
            house=house,
            properties=properties,
            balance=balance,
            order=order)

    def buy(self, property):
        if (self.balance - property.purchase_price) >= 80:
            self.balance -= property.purchase_price
            self.properties.append(property)
            property.owner = self
            self.player_info['buy_payments'].append(property.purchase_price)
        return True
