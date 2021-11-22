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
        '''
        Calcula o índice do próximo jogador a jogar.
        :return: Número correspondente à key do próximo jogador no
                 dicinoário de jogadores.
        '''
        next = self.actual_player + 1
        if next > len(self.players.keys()):
            # Somente para o caso do próximo jogador estar além dos que estão
            # no jogo, eu volto pro começo.
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

    def update_player_house(self, player_to_update, final_house, back_to_init=False):
        '''
        Aqui é onde eu faço a movimentação do jogador no tabuleiro.
        :param player_to_update: Jogador que terá sua posição atualizada
        :param final_house: número (índice) da casa final
        :param back_to_init: Flag indicativo se houve retorno ao começo do tabuleiro
        '''
        # Removo o jogador da lista de jogadores da casa antiga dele
        self.houses[player_to_update.house].players.remove(player_to_update)
        # Atualizo, no jogador, a posição da nova casa
        player_to_update.house = final_house
        # Adiciono o jogador à lista de jogadores da casa nova
        self.houses[final_house].players.append(player_to_update)
        if back_to_init:
            # No caso de conseguir voltar ao começo, pago 100 a ele.
            player_to_update.balance += 100
            player_to_update.player_info['lap_counter'] += 1

    def next_play(self):
        '''Realiza a próxima jogada (ou a do próximo lançamento...'''
        # Pegando o jogador da vez
        player = self.players[self.actual_player]
        # Aqui eu jogo o dado
        dice = numpy.random.randint(low=1, high=7)
        # Localizo a casa sorteada
        next_house, back_to_init = player.get_next_house(
            dice, len(self.houses.keys()) - 1)
        # Faço a movimentação do jogador no tabuleiro
        self.update_player_house(player, next_house, back_to_init)

        # Aqui checo se tem propriedade definida nesta casa
        if self.houses[next_house].property is not None:
            # Realizando a operação (compra ou aluguel)
            operation_result = player.buy_or_rent(self.houses[next_house].property)
            # Resultado falho correponde ao caso de saldo negativo após a
            # operação. Neste caso, ocorre a saída do jogo por derrota.
            if not operation_result:
                # Jogador perde todas as propriedades
                player.lose_all()
                # No extrato de movimentos do jogador, marco o último round dele
                player.player_info['last_round'] = self.round
                # Marco que o jogador saiu por derrota do jogo
                player.player_info['status'] = 'looser'
                # Salvo o extrato do jogador no extrato da partida, pois o
                # jogador irá desaparecer bem aqui....
                self.players_report_info[player.name] = player.player_info
                # Bye, bye!!!
                self.remove_player(player)

        # Atualizo o ponteiro para o jogador da vez
        self.actual_player = self.get_next_player()
        # Atualizo o contador de rounds (necessário para o cálculo da
        # média de rounds por partida ao final da simulação.
        self.round += 1

    def has_winner(self):
        '''
            Checa se tem vencedor da partida. Caso tenha, a partida deverá ser encerrada
        imediatamente.
        :return: Dados do jogador vencedor (o encontrado) ou None.
        '''
        if len(self.players.keys()) == 1:
            # O reconhecimento de um vencedor ocorre sempre que, ao fim de um
            # movimento, é detectado somente um jogador no tabuleiro.
            # Vale ressaltar que o jogador é removido do jogo assim que, ao fim
            # de uma operação, é detectado que o mesmo ficou com saldo negativo.
            self.players[1].player_info['last_round'] = self.round
            self.players[1].player_info['status'] = 'winner'
            self.players_report_info[self.players[1].name] = self.players[1].player_info
            return self.players[1]
        return None
