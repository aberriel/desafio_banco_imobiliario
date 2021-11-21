class House:
    def __init__(self, position, players=None, property=None):
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
