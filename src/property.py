class Property:
    '''Propriedade (imóvel) que estará alocado em alguma casa do tabuleiro'''
    def __init__(self, purchase_price, rent_amount, name='', owner=None, house=None):
        '''
        Construtor da classe
        :param purchase_price: Preço de venda do imóvel
        :param rent_amount: Valor que pode ser obtido com o pagamento de aluguéis
        :param name: Um nome pra propriedade
        :param owner: Jogador proprietário da propriedade
        :param house: Casa do tabuleiro onde a propriedade estará
        '''
        self.purchase_price = purchase_price
        self.rent_amount = rent_amount
        self.name = name
        self.owner = owner
        self.house = house

    def __str__(self):
        return f'{self.name} | C: R${self.purchase_price} | A: R${self.rent_amount}' \
            if self.name and len(self.name) > 0 \
            else f'C: R${self.purchase_price} | A: R${self.rent_amount}'

    def to_json(self):
        return {
            'owner': self.owner.name if self.owner is not None else 'NO OWNER',
            'purchase_price': self.purchase_price,
            'rent_amount': self.rent_amount,
            'name': self.name,
            'house': self.house
        }
