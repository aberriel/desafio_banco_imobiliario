class Player:
    def __init__(self, name, properties=None, house=0, balance=300, order=0):
        self.name = name
        self.house = house
        self.properties = properties or []
        self.balance = balance
        self.ordem = order or 0
        self.player_info = {
            'last_round': None,
            'status': None,
            'buy_payments': [],
            'rent_payments': [],
            'amounts_received': []}

    def buy(self, property):
        pass

    def rent(self, property):
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

    def buy_or_rent(self, property):
        if property is None:
            return True
        return self.buy(property) \
            if property.owner is None \
            else self.rent(property)

    def lose_all(self):
        for pr in self.properties:
            pr.owner = None

    def get_next_house(self, houses_to_go, total_houses):
        final_house = self.house + houses_to_go
        if final_house > total_houses:
            final_house = self.house + houses_to_go - total_houses - 1
        return final_house
