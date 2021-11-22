from .player_base import Player


class ImpulsivePlayer(Player):
    '''Implementação para o comportamento impulsivo.'''
    def __init__(self, properties=None, house=0, balance=300, name='Impulsive', order=0):
        super(ImpulsivePlayer, self).__init__(
            name=name,
            house=house,
            properties=properties,
            balance=balance,
            order=order)

    def buy(self, property):
        '''
        Processo de compra para o jogador impulsivo.
        Neste caso, ele irá comprar o que estiver disponível onde ele pisar.
        Presume-se que será quase sempre o primeiro jogador a sair do tabuleiro.
        :param property: Propriedade envolvida na transação.
        :return: Flag indicador se a operação foi bem-sucedida ou o jogador
                 perdeu a partid
        '''
        self.balance -= property.purchase_price
        if self.balance < 0:
            return False
        self.properties.append(property)
        property.owner = self
        self.player_info['buy_payments'].append(property.purchase_price)
        return True
