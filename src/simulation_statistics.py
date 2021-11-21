class Statistics:
    def __init__(self, data_set: list):
        self.data_set = data_set

        self.players_statistics = {}
        for player_name in self.data_set[0]['players_info'].keys():
            self.players_statistics[player_name] = {
                'win_percent': 0,
                'win_count': 0,
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
        for player_type in self.players_statistics.keys():
            for player_info in self.players_statistics[player_type].keys():
                self.players_statistics[player_type][player_info] = 0

    def count_finances(self):
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
        total = 0
        for item in self.data_set:
            if item['status'] == 'finished_by_timeout' and item['total_rounds'] >= 1000:
                total += 1
        return total

    def run(self):
        self.reset_player_stats()
        rounds_average = sum(item.get('total_rounds', 0) for item in self.data_set) / len(self.data_set)
        self.count_winners()
        self.count_finances()
        most_frequent_wins, win_count = self.most_frequent_winner()
        return {
            'rounds_average': rounds_average,
            'finished_by_timeout': self.total_games_finished_by_timeout(),
            'players_statistics': self.players_statistics,
            'most_frequent_winners': {
                'player_types': most_frequent_wins,
                'win_count': win_count
            }}
