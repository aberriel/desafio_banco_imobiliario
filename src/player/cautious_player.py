from .player_base import Player


class CautiousPlayer(Player):
    '''Implementação para o comportamento cauteloso.'''
    def __init__(self, properties=None, house=0, balance=300, name='Cautelous', order=0):
        super(CautiousPlayer, self).__init__(
            name=name,
            house=house,
            properties=properties,
            balance=balance,
            order=order)

    def buy(self, property):
        '''
        Processo de compra para o jogador cauteloso.
        Neste caso, a compra só é efetivada caso o saldo final após a transação
        seja maior ou igual a 80.

        Assim, nunca poderá ocorrer a derrota por compra demasiada mas somente
        pelo pagamento de muitos aluguéis.
        :param property: Propriedade envolvida na transação.
        :return: Flag indicador se a operação foi bem-sucedida ou o jogador
                 perdeu a partida.
        '''
        if (self.balance - property.purchase_price) >= 80:
            # Operação de compra só é realizada caso o saldo após a operação
            # seja maior ou igual a 80.
            self.balance -= property.purchase_price
            self.properties.append(property)
            property.owner = self
            self.player_info['buy_payments'].append(property.purchase_price)
        return True
