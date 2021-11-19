class Property:
    def __init__(self, purchase_price, rent_amount, name='', owner=None, house=None):
        self.purchase_price = purchase_price
        self.rent_amount = rent_amount
        self.name = name
        self.owner = owner
        self.house = house

    def __str__(self):
        return f'{self.name} | C: R${self.purchase_price} | A: R${self.rent_amount}' \
            if self.name else f'C: R${self.purchase_price} | A: R${self.rent_amount}'
