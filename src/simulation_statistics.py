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