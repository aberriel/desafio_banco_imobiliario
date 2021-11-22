#! /usr/bin/env python

import os
if 'src' in os.getcwd():
    from config import Config
    from simulation import Simulation
    from simulation_statistics import Statistics
else:
    from src.config import Config
    from src.simulation import Simulation
    from src.simulation_statistics import Statistics


def collect_data(total_tests, print_data=True, properties_dict=None):
    '''
    Realiza a etapa inicial do ETC (modelagem do que será construído).
    :param total_tests: Total de testes (execução da simulação) serão aceitos.
    :param print_data: Flag que indica se quero imprimir no console o resultado
                       final de cada round.
                       Coloquei como opção para permitir testar sem ter o console
                       poluído.
    :param properties_dict: Dict contendo a configuração das propriedades a serem
                            utilizadas no jogo.
    :return:
    '''
    result_list = []
    count = 0
    if not properties_dict:
        # Se não defini nenhuma configuração de propriedades, utilizo
        # a que possui os menores valores
        c = Config()
        properties_dict = c.properties_5
    while count < total_tests:
        # Aqui executo a simulação de uma partida completa
        simulation = Simulation(game_config=properties_dict)
        result = simulation.run()

        if print_data:
            # Só se quero exibir o resultado da partida no console.
            final_status = 'TIMEOUT' \
                if result['status'] == 'finished_by_timeout' else 'WINNER'
            winner = result['winner'] if result['winner'] is not None \
                else 'TH'
            print(f'({count + 1}) ROUNDS {result["total_rounds"]} | '
                  f'WINNER {winner} | STATUS {final_status}')

        # Guardo o resultado desta simulação. E parto pra próxima.
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

    :param total_rounds: Total de execuções da simulação.
                         Por default coloquei 10 (permite tirar a prova
                         dos 9 na mão).
    '''
    c = Config()
    # Realizo a simulação
    simulation_data = collect_data(total_tests=total_tests,
                                   print_data=False,
                                   properties_dict=c.properties_4)
    # Calculo as estatísticas
    processor = Statistics(data_set=simulation_data)
    statistics = processor.run()

    # Exibindo as estatísticas no console
    print('\n')
    print('====================================================================================')
    print('================================ Estatísticas ======================================')
    print('====================================================================================')
    print('\n')

    print(f'* Partidas terminadas por timeout: {statistics["finished_by_timeout"]}')
    print(f'* Duração média da partida: {statistics["rounds_average"]} turnos')
    print(f'* Porcentagem de vitória por comportamento dos jogadores: ')
    for player_type in statistics['players_statistics'].keys():
        print(f'\t+ {player_type} - {statistics["players_statistics"][player_type]["win_percent"]}%')
    print(f'* Comportamento(s) que mais vence(m): {", ".join(statistics["most_frequent_winners"]["player_types"])}')

    return statistics


if __name__ == '__main__':
    main(300)
