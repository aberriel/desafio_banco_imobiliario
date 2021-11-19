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
        # print(f'CautiousPlayer.buy -> Entrando para property {property.nome}')
        # print(f'CautiousPlayer.buy -> Casa da property: {property.house}')
        # print(f'CautiousPlayer.buy -> Valor de compra: {property.valor_compra}')
        # print(f'CautiousPlayer.buy -> Saldo inicial: {self.saldo}')
        if (self.balance - property.purchase_price) >= 80:
            # print(f'CautiousPlayer.buy -> Comprando property {property.nome}')
            self.balance -= property.purchase_price
            self.properties.append(property)
            property.owner = self
        # print(f'CautiousPlayer.buy -> Saldo final: {self.saldo}')
        return True
