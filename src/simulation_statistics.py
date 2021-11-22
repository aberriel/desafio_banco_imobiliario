class Statistics:
    '''
    Classe para processamento de dados de resultado de jogo e geração
    das estatísticas.
    '''
    def __init__(self, data_set: list):
        '''
        Aqui recebo os dados de uma série de simulações e os preparo para
        realizar a análise.
        :param data_set: Conjunto de dados de uma série de simulações.
        '''
        self.data_set = data_set

        self.players_statistics = {}
        for player_name in self.data_set[0]['players_info'].keys():
            self.players_statistics[player_name] = {
                'win_percent': 0,
                'win_count': 0,
                'lap_count': 0,
                'buy_payments_count': 0,
                'buy_payments_count_average': 0,
                'buy_payments_sum': 0,
                'buy_payments_average': 0,
                'rent_payments_count': 0,
                'rent_payments_count_average': 0,
                'rent_payments_sum': 0,
                'rent_payments_average': 0,
                'rent_received_count': 0,
                'rent_received_count_average': 0,
                'rent_received_sum': 0,
                'rent_received_average': 0}

    def reset_player_stats(self):
        '''
        Para o caso de ter ocorrido alguma alteração nas estatísticas do jogo
        entre a instanciação da classe e a execução da análise (chamada do run()),
        eu posso por este método zerar todas as estatísticas antes de realizar
        uma nova análise.
        :return:
        '''
        for player_type in self.players_statistics.keys():
            for player_info in self.players_statistics[player_type].keys():
                self.players_statistics[player_type][player_info] = 0

    def count_finances(self):
        '''
        Aqui eu realizo a análise dos comportamentos em termos de compra,
        pagamento de aluguel e recebimento do mesmo.

        A idéia é associar o status final de um jogador (tanto em termos se
        ganhou ou perdeu quanto o tempo - número de rounds - que demorou a
        sair do jogo) com o seu resultado, identificando as nuances do
        comportamento que o levou a ganhar ou perder a partida.
        '''
        for data_item in self.data_set:
            for player_item in data_item['players_info'].keys():
                self.players_statistics[player_item]['buy_payments_count'] += \
                    len(data_item['players_info'][player_item]['buy_payments'])
                self.players_statistics[player_item]['buy_payments_sum'] += \
                    sum(data_item['players_info'][player_item]['buy_payments'])
                self.players_statistics[player_item]['rent_payments_count'] += \
                    len(data_item['players_info'][player_item]['rent_payments'])
                self.players_statistics[player_item]['rent_payments_sum'] += \
                    sum(data_item['players_info'][player_item]['rent_payments'])
                self.players_statistics[player_item]['rent_received_count'] += \
                    len(data_item['players_info'][player_item]['amounts_received'])
                self.players_statistics[player_item]['rent_received_sum'] += \
                    sum(data_item['players_info'][player_item]['amounts_received'])

        for player_type in self.players_statistics.keys():
            self.players_statistics[player_type]['buy_payments_count_average'] = \
                self.players_statistics[player_type]['buy_payments_count'] / len(self.data_set)
            self.players_statistics[player_type]['buy_payments_average'] = \
                self.players_statistics[player_type]['buy_payments_sum'] / len(self.data_set)
            self.players_statistics[player_type]['rent_payments_count_average'] = \
                self.players_statistics[player_type]['rent_payments_count'] / len(self.data_set)
            self.players_statistics[player_type]['rent_payments_average'] = \
                self.players_statistics[player_type]['rent_payments_sum'] / len(self.data_set)
            self.players_statistics[player_type]['rent_received_count_average'] = \
                self.players_statistics[player_type]['rent_received_count'] / len(self.data_set)
            self.players_statistics[player_type]['rent_received_average'] = \
                self.players_statistics[player_type]['rent_received_sum'] / len(self.data_set)

    def count_winners(self):
        '''
        Realiza a contabilidade das vitórias por comportamento, tanto em termos
        de contagem quanto em termos percentuais.
        '''
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
        '''
        Realiza o cálculo do vencedor mais frequente a partir dos dados das
        vitórias por perfil já processados.
        :return: Lista de jogadores com o número máximo de vitórias (para o caso
                 de haver mais de um com o número maior de vitórias) e o contador
                 de vitórias para o(s) perfil(is) detectado(s).
        '''
        # Variável para controle do maior número de vitórias encontrado
        win_count = 0
        # Posso ter mais de um ganhador frequente. Então fico com um array.
        players = []
        for item in self.players_statistics.keys():
            player_win_count = self.players_statistics[item]['win_count']
            if player_win_count > win_count:
                players = []
                players.append(item)
                win_count = player_win_count
            elif player_win_count == win_count:
                # Aqui entro no caso em que 2 ou mais tem o máximo de vitórias...
                players.append(item)
        return players, win_count

    def mount_players_statistics(self):
        self.count_winners()

    def total_games_finished_by_timeout(self):
        '''
        Realizo a contagem de partidas finalizadas por timeout.
        :return: Contador de partidas finalizadas por timeout (1000 ou mais jogadas)
                 detectado nos dados
        '''
        total = 0
        for item in self.data_set:
            if item['status'] == 'finished_by_timeout' and item['total_rounds'] >= 1000:
                total += 1
        return total

    def run(self):
        '''
        Aqui é onde realizo o processo de análise, que consiste em:

            1 - Calcular a média de rounds por partida para toda a simulação
            2 - Realizar as contagens de vitória com percentual para cada tipo
                de jogador
            3 - Determinar os indicadores financeiros (comportamentos em termo de compras,
                vendas e recebimento de alugueis) por perfil de jogador
            4 - Extrair o vencedor mais frequente (o que possui percentual maior de
                vitórias ou tem o contador de vitórias com valor maior que todos
        :return: Extrato da simulação, com os dados acima.
        '''
        # Resetando os contadores antes da análise
        self.reset_player_stats()
        # Calculando a média de rounds por partida na simulação
        rounds_average = sum(item.get('total_rounds', 0) for item in self.data_set) / len(self.data_set)
        # Fazendo a contagem de vencedores por número de partidas
        self.count_winners()
        # Gerando os contadores financeiros
        self.count_finances()
        # Determinando o vencedor mais frequente, junto com o contador de
        # vitórias dele
        most_frequent_wins, win_count = self.most_frequent_winner()
        # Retornando o extrato para exibição.
        return {
            'rounds_average': rounds_average,
            'finished_by_timeout': self.total_games_finished_by_timeout(),
            'players_statistics': self.players_statistics,
            'most_frequent_winners': {
                'player_types': most_frequent_wins,
                'win_count': win_count
            }}
