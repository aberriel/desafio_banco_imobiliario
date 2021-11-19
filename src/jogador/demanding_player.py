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
        # print(f'DemandingPlayer.buy -> Entrando para property {property.nome}')
        # print(f'DemandingPlayer.buy -> Casa da property: {property.house}')
        # print(f'DemandingPlayer.buy -> Valor do aluguel da property: {property.valor_aluguel}')
        # print(f'DemandingPlayer.buy -> Valor de compra: {property.valor_compra}')
        # print(f'DemandingPlayer.buy -> Saldo inicial: {self.saldo}')
        if property.rent_amount > 50:
            self.balance -= property.purchase_price
            if self.balance < 0:
                # print(f'DemandingPlayer.buy -> Saindo do game por saldo negativo')
                return False
            self.properties.append(property)
            property.owner = self
        # print(f'DemandingPlayer.buy -> Saldo final: {self.saldo}')
        return True
