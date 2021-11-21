from .player_base import Player


class DemandingPlayer(Player):
    def __init__(self, properties=None, house=0, balance=300, name='Demanding', order=0):
        super(DemandingPlayer, self).__init__(
            name=name,
            house=house,
            properties=properties,
            balance=balance,
            order=order)

    def buy(self, property):
        if property.rent_amount > 50:
            self.balance -= property.purchase_price
            if self.balance < 0:
                return False
            self.properties.append(property)
            property.owner = self
            self.player_info['buy_payments'].append(property.purchase_price)
        return True
