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
        # print(f'ImpulsivePlayer.buy -> Entrando para property {property.nome}')
        # print(f'ImpulsivePlayer.buy -> Casa da property: {property.house}')
        # print(f'ImpulsivePlayer.buy -> Valor da property: {property.valor_compra}')
        # print(f'ImpulsivePlayer.buy -> Saldo inicial: {self.saldo}')
        self.balance -= property.purchase_price
        if self.balance < 0:
            # print(f'JogadorImpulsivo.compra -> Saindo por saldo negativo')
            return False
        self.properties.append(property)
        property.owner = self
        # print(f'JogadorImpulsivo.compra -> Saldo final: {self.saldo}')
        return True
