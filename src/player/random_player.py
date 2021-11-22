from .player_base import Player
import numpy


class RandomPlayer(Player):
    '''
    Model para o jogador do tipo "random".
    O jogador Random é o que não decide apenas com base no tempo ou outro algo aleatório...
    '''
    def __init__(self, properties=None, house=0, balance=300, name='Random', order=0):
        '''
        Construtor da classe
        :param properties:
        :param house: Casa onde o player está
        :param balance: Saldo total da conta do player
        :param name: Nome do player
        :param order:
        '''
        super(RandomPlayer, self).__init__(
            name=name,
            house=house,
            properties=properties,
            balance=balance,
            order=order)

    def buy(self, property):
        '''
        Peocesso de compra para o jogador aleatório.
        Neste caso, uma moeda não viciada decidirá se irá comprar ou não.
        :param property: Propriedade envolvida na transação.
        :return: Flag indicador se a operação foi bem-sucedida ou o jogador
                 perdeu a partid
        '''
        can_buy = numpy.random.randint(low=0, high=2)
        if can_buy == 1:
            self.balance -= property.purchase_price
            if self.balance < 0:
                return False
            self.properties.append(property)
            property.owner = self
            self.player_info['buy_payments'].append(property.purchase_price)
        return True
