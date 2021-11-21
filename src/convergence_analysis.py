from .config import Config
from .simulation import Simulation


def main(total_tests):
    result_list = []
    count = 0
    while count < total_tests:
        c = Config()
        simulation = Simulation(game_config=c.properties_5)
        result = simulation.run()
        result_list.append(result)
        count += 1
    return result_list
