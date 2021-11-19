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
        # print(f'RandomPlayer.buy -> Entrando para property {property.nome}')
        # print(f'RandomPlayer.buy -> Casa da property: {property.house}')
        # print(f'RandomPlayer.buy -> Valor da property: {property.valor_compra}')
        # print(f'RandomPlayer.buy -> Saldo inicial: {self.saldo}')
        can_buy = numpy.random.randint(low=0, high=2)
        # print(f'JogadorAleatorio.compra -> Decisão de comprar: {can_buy}')
        if can_buy == 1:
            self.balance -= property.purchase_price
            if self.balance < 0:
                # print(f'RandomPlayer.buy -> Saindo do game por saldo negativo')
                return False
            self.properties.append(property)
            property.owner = self
        # print(f'JogadorAleatorio.compra -> Saldo final: {self.saldo}')
        return True
