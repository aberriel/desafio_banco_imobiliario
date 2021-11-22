import os
if 'src' in os.getcwd():
    from house import House
    from property import Property
    from utils import make_players_with_aleatory_order
else:
    from src.house import House
    from src.property import Property
    from src.utils import make_players_with_aleatory_order
import numpy


class Game:
    '''
        Classe que define os elementos relacionados ao jogo.
        Esta classe também pode ser dada como equivalente ao tabuleiro do jogo (mas também
    possui os métodos relacionados à movimentação do jogo e ao encerramento de partida do
    jogo, com retorno do vencedor cjo haja.
    '''
    game_report = dict()

    def __init__(self, round=0, players=None, houses=None, actual_player=1):
        '''
        Construtor da classe
        :param round: Número do round atual desde o começo da partida
        :param players: Jogadores que estão participando.
                        Vale considerar que quando um jogador sai do jogo, ele é (ou
                        deverá ser) removido da lista de jogadores da partida.
        :param houses: Casas do tabuleiro, que podem conter uma propriedade ou não.
        :param actual_player: Número (índice) do jogador atual da partida, o que tem
                              o ves.
        '''
        self.round = round
        self.players = players or dict()
        self.houses = houses or dict()
        self.actual_player = actual_player or 1
        self.players_report_info = {}

        if len(self.players.keys()) == 0:
            self.players = make_players_with_aleatory_order()

        if len(self.houses.keys()) == 0:
            self.make_random_houses()

        self.arrange_players_houses()

    def _prepare_report(self):
        self.game_report = {
            'players': {}
        }

        for pointer in self.players.keys():
            self.game_report['players'][pointer] = {
                'name': self.players[pointer]['name'],
                'order': pointer
            }

    def make_random_houses(self):
        counter = 0
        while counter <= 20:
            house = House(position=counter)
            if counter > 0:
                purchase_price = numpy.random.randint(low=2, high=301)
                rent_amount = numpy.random.randint(low=0, high=purchase_price/2)
                if rent_amount == 0:
                    rent_amount = 1
                property = Property(
                    purchase_price=purchase_price,
                    rent_amount=rent_amount,
                    name=f'Casa {counter}',
                    house=counter)
                house.property = property
            self.houses[counter] = house
            counter += 1

    def arrange_players_houses(self):
        for player_position in self.players.keys():
            self.houses[0].players.append(self.players[player_position])
            self.players[player_position].house = 0

    def get_next_player(self):
        next = self.actual_player + 1
        if next > len(self.players.keys()):
            next = 1
        return next

    def remove_player(self, player_to_delete):
        '''
        Remove jogador da lista de jogadores ativos na partida.
        :param player_to_delete: player_to_delete
        '''
        self.houses[player_to_delete.house].players.remove(player_to_delete)
        del self.players[player_to_delete.order]

        # Agora vamos reestruturar os players
        counter = 1
        dict_players_2 = dict()
        for item in self.players.keys():
            dict_players_2[counter] = self.players[item]
            dict_players_2[counter].order = counter
            counter += 1
        self.players = dict_players_2

    def update_player_house(self, player_to_update, final_house):
        self.houses[player_to_update.house].players.remove(player_to_update)
        player_to_update.house = final_house
        self.houses[final_house].players.append(player_to_update)

    def next_play(self):
        '''Realiza a próxima jogada (ou a do próximo lançamento...'''
        player = self.players[self.actual_player]
        dice = numpy.random.randint(low=1, high=7)
        next_house = player.get_next_house(dice, len(self.houses.keys()) - 1)
        self.update_player_house(player, next_house)

        if self.houses[next_house].property is not None:
            operation_result = player.buy_or_rent(self.houses[next_house].property)
            if not operation_result:
                player.lose_all()
                player.player_info['last_round'] = self.round
                player.player_info['status'] = 'looser'
                self.players_report_info[player.name] = player.player_info
                self.remove_player(player)

        self.actual_player = self.get_next_player()
        self.round += 1

    def has_winner(self):
        '''
            Checa se tem vencedor da partida. Caso tenha, a partida deverá ser encerrada
        imediatamente.
        :return: Dados do jogador vencedor (o encontrado) ou None.
        '''
        if len(self.players.keys()) == 1:
            self.players[1].player_info['last_round'] = self.round
            self.players[1].player_info['status'] = 'winner'
            self.players_report_info[self.players[1].name] = self.players[1].player_info
            return self.players[1]
        return None
