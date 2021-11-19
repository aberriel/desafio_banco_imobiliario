class Player:
    def __init__(self, name, properties=None, house=0, balance=300, order=0):
        self.name = name
        self.house = house
        self.properties = properties or []
        self.balance = balance
        self.ordem = order or 0

    def buy(self, property):
        pass

    def rent(self, property):
        # print(f'Player.rent -> Entrando para property {property.nome}')
        if property.owner == self:
            # Se o proprietário sou eu, não tem o que fazer, né?
            return True
        # Pago o aluguel
        # print(f'Player.rent -> Tentando pagar o aluguel {property.valor_aluguel} do player {self.nome}')
        self.balance -= property.rent_amount
        if self.balance < 0:
            # Nem dou o aluguel ao proprietário. O infeliz aqui não tem dinheiro.
            # print(f'Jogador.aluga -> Jogador {self.nome} perdeu por saldo negativo')
            return False
        # O proprietário recebe o aluguel
        # print(f'Jogador.aluga -> Pagando o aluguel {property.valor_aluguel} ao player {property.proprietario.nome}')
        property.owner.balance += property.rent_amount
        return True

    def buy_or_rent(self, property):
        # print('Player.buy_or_rent -> Entrando')
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
