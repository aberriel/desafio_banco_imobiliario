from .player_base import Player


class DemandingPlayer(Player):
    '''Implementação para o comportamento exigente'''
    def __init__(self, properties=None, house=0, balance=300, name='Demanding', order=0):
        super(DemandingPlayer, self).__init__(
            name=name,
            house=house,
            properties=properties,
            balance=balance,
            order=order)

    def buy(self, property):
        '''
        Processo de compra para o jogador exigente.
        Neste caso, o jogador só efetuará a compra caso o valor do aluguel
        ultrapasse um mínimo exigido por ele (definido como 50).

        Este comportamento trará mais retornos, porém, os gastos serão maiores, pois
        aluguéis maiores serão sempre das propriedades mais caras.
        :param property:
        :return:
        '''
        if property.rent_amount > 50:
            self.balance -= property.purchase_price
            if self.balance < 0:
                return False
            self.properties.append(property)
            property.owner = self
            self.player_info['buy_payments'].append(property.purchase_price)
        return True
