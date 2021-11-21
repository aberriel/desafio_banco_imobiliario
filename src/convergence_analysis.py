from .config import Config
from .simulation import Simulation


class Statistics:
    def __init__(self, data_set: list):
        self.data_set = data_set

        self.players_statistics = {}
        for player_name in self.data_set[0]['players_info'].keys():
            self.players_statistics[player_name] = {
                'win_percent': 0,
                'win_count': 0,
                'total_win_rounds_average': 0,
                'buy_payments_count_average': 0,
                'buy_payments_average': 0,
                'rent_payments_count_average': 0,
                'rent_payments_average': 0,
                'rent_received_count_average': 0,
                'rent_received_average': 0}

    def count_finances(self):
        consolidated = dict()
        for player_name in self.data_set[0]['players_info'].keys():
            consolidated[player_name] = {
                'buy_payments_count': 0,
                'buy_payments_sum': 0,
                'rent_received_count': 0,
                'rent_received_sum': 0,
                'rent_payments_count': 0,
                'rent_payments_sum': 0
            }

        for data_item in self.data_set:
            for player_item in data_item['players_info'].keys():
                consolidated[player_item]['buy_payments_count'] += len(data_item['players_info'][player_item]['buy_payments'])
                consolidated[player_item]['buy_payments_sum'] += sum(data_item['players_info'][player_item]['bui_payments'])
                consolidated[player_item]['rent_payments_count'] += len(data_item['players_info'][player_item]['buy oayments'])
                consolidated[player_item]['rent_received_count'] += len(data_item['players_info'][player_item]['amounts_received'])

    def count_winners(self):
        # Contabilizando as vitórias por tipo de comportamento
        win_total = 0
        for item in self.data_set:
            if item['status'] == 'finished_by_winner' and item['winner'] is not None:
                self.players_statistics[item["winner"]]['win_count'] += 1
                # Contabilizando o total de finalizações por vitória
                win_total += 1

        # Agora contabilizando os percentuais
        for p_item in self.players_statistics.keys():
            self.players_statistics[p_item]['win_percent'] = \
                self.players_statistics[p_item]['win_count'] / win_total * 100.0

    def most_frequent_winner(self):
        win_count = 0
        players = []
        for item in self.players_statistics.keys():
            player_win_count = self.players_statistics[item]['win_count']
            if player_win_count > win_count:
                players = []
                players.append(item)
                win_count = player_win_count
            elif player_win_count == win_count:
                players.append(item)
        return players, win_count

    def mount_players_statistics(self):
        self.count_winners()

    def total_games_finished_by_timeout(self):
        total = 0
        for item in self.data_set:
            if item['status'] == 'finished_by_timeout' and item['total_rounds'] >= 1000:
                total += 1

    def run(self):
        rounds_average = sum(item.get('total_rounds', 0) for item in self.data_set) / len(self.data_set)
        finished_by_timeout = self.total_games_finished_by_timeout()
        return {
            'rounds_average': rounds_average,
            'finished_by_timeout': finished_by_timeout,
            'players_statistics': self.players_statistics}


def collect_data(total_tests, print_data=True, properties_dict=None):
    result_list = []
    count = 0
    while count < total_tests:
        if not properties_dict:
            c = Config()
            properties_dict = c.properties_5
        simulation = Simulation(game_config=properties_dict)
        result = simulation.run()

        if print_data:
            final_status = 'TIMEOUT' \
                if result['status'] == 'finished_by_timeout' else 'WINNER'
            winner = result['winner'] if result['winner'] is not None \
                else 'TH'
            print(f'({count + 1}) ROUNDS {result["total_rounds"]} | '
                  f'WINNER {winner} | STATUS {final_status}')

        result_list.append(result)
        count += 1
    return result_list


def main(total_tests=10):
    '''
    Esta função realiza a estatística pedida, que consiste em:

        - Cálculo de partidas terminadas por timeout (número e percentual)
        - Média de turnos por partida
        - Percentual de vitória por tipo de comportamento (ou jogador)
        - Determinação do comportamento mais vitorioso (o dado acima já mostrará isso)

    Esta análise rodará sobre o set de dados 4, o de menor valor variável para os imóveis.

    :param total_rounds: Total de execuções da simulação
    '''
    c = Config()
    simulation_data = collect_data(total_tests=total_tests, print_data=True, properties_dict=c.properties_4)
    processor = Statistics(data_set=simulation_data)
    return processor


def main_2(total_tests=10):
    '''
    Esta função executará a análise acima considerando todos os 4 sets de dados, realizando
    um comparativo das análises pedidas para os sets considerando:

        - Valor base (properties_1)
        - 50%
        - 25%
        - 12,5%
        - Valores fixos e iguais para todos em 5 (compra) e 2 (aluguel)

    A análise consistirá em um comparativo dos dados pedidos para os 5 sets de dados.

    :param total_rounds:
    :return:
    '''
    c = Config()
    simulation_properties_1 = collect_data(
        total_tests=total_tests,
        print_data=False,
        properties_dict=c.properties)
    processor_1 = Statistics(data_set=simulation_properties_1)
    statistics_1 = processor_1.run()

    simulation_properties_2 = collect_data(
        total_tests=total_tests,
        print_data=False,
        properties_dict=c.properties_2)
    processor_2 = Statistics(data_set=simulation_properties_2)
    statistics_2 = processor_2.run()

    simulation_properties_3 = collect_data(
        total_tests=total_tests,
        print_data=False,
        properties_dict=c.properties_3)
    processor_3 = Statistics(data_set=simulation_properties_3)
    statistics_3 = processor_3.run()

    simulation_properties_4 = collect_data(
        total_tests=total_tests,
        print_data=False,
        properties_dict=c.properties_4)
    processor_4 = Statistics(data_set=simulation_properties_4)
    statistics_4 = processor_4.run()

    simulation_properties_5 = collect_data(
        total_tests=total_tests,
        print_data=False,
        properties_dict=c.properties_5)
    processor_5 = Statistics(data_set=simulation_properties_5)
    statistics_5 = processor_5.run()


def main_3():
    '''
    Esta função realizará a análise ce convergência dos dados, variando de 300 até 1 milhão
    para o set de dados 4 (12,5%).
    :return:
    '''
    pass


if __name__ == '__main__':
    pass
