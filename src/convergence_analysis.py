from .simulation import Simulation


def main(total_tests):
    result_list = []
    count = 0
    while count < total_tests:
        simulation = Simulation()
        result = simulation.run()
        result_list.append(result)


if __name__ == '__main__':
    main(10)
