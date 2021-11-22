class House:
    '''Esta classe é, por definição, a casa do tabuleiro do jogo.'''
    def __init__(self, position, players=None, property=None):
        '''
        Construtor da classe
        :param position: Posição que a casa ocupa no tabuleiro
        :param players: Jogadores que estão ocupando esta casa
        :param property: Propriedade que está nesta casa.
        '''
        self.position = position
        self.players = players or []
        self.property = property

    def __str__(self):
        property_name = self.property.name \
            if self.property is not None and self.property.name is not None \
            else 'NO NAME'
        return f'({self.position}) (P: {property_name}) {len(self.players)} Players'

    def __repr__(self):
        return self.__str__()
