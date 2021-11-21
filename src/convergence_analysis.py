from .config import Config
from .simulation import Simulation
from .simulation_statistics import Statistics


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


if __name__ == '__main__':
    pass
