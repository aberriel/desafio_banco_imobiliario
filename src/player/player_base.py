class Player:
    '''Classe base para todos os tipos de jogadores'''
    def __init__(self, name, properties=None, house=0, balance=300, order=0):
        '''
        Construtor da classe
        :param name: Nome do tipo de jogador
        :param properties: Lista de propriedades adquiridas ao longo da partida
        :param house: Casa do tabuleiro onde o jogador se encontra
        :param balance: Saldo atual do jogador
        :param order: Ordem de jogada
        '''
        self.name = name
        self.house = house
        self.properties = properties or []
        self.balance = balance
        self.order = order or 0
        self.player_info = {
            'last_round': None,
            'status': None,
            'lap_counter': 0,
            'buy_payments': [],
            'rent_payments': [],
            'amounts_received': []}

    def buy(self, property):
        pass

    def rent(self, property):
        '''
        Método para a operação de aluguel
        :param property: Propriedade envolvida na transação
        :return: Flag indicando o sucesso na operação ou se o jogador perdeu.
        '''
        if property.owner == self:
            # Se o proprietário sou eu, não tem o que fazer, né?
            return True
        # Pago o aluguel
        self.balance -= property.rent_amount
        if self.balance < 0:
            # Nem dou o aluguel ao proprietário. O infeliz aqui não tem dinheiro.
            return False
        # O proprietário recebe o aluguel
        property.owner.balance += property.rent_amount
        property.owner.player_info['amounts_received'].append(property.rent_amount)
        self.player_info['rent_payments'].append(property.rent_amount)
        return True

    def buy_or_rent(self, property=None):
        '''
        Determina se é a compra ou aluguel que está habilitado
        :param property: Propriedade pra rolo
        :return: Resultado da operação (compra ou aluguel) realizada
        '''
        if property is None:
            # Se não há propriedade, não há o que fazer, né?
            return True
        return self.buy(property) \
            if property.owner is None \
            else self.rent(property)

    def lose_all(self):
        '''Aqui removo todas as propriedades por derrota no jogo'''
        for pr in self.properties:
            pr.owner = None

    def get_next_house(self, house_to_go, total_houses):
        '''
        Realiza o cálculo da próxima casa e determina se houve um retorno ao
        começo do tabuleiro, para pagar os 100 pela volta completada
        :param house_to_go: Número da casa para onde deve ir
        :param total_houses: Total de casas no tabuleiro
        :return: Número da casa final e o indicativo se houve volta completada
                 no tabuleiro.
        '''
        back_to_init = False
        final_house = self.house + house_to_go
        if final_house > total_houses:
            final_house = self.house + house_to_go - total_houses - 1
            back_to_init = True
        return final_house, back_to_init
