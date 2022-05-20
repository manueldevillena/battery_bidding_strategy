
from optimise_battery.core import CreateInputs, Simulate
from utils import plot_market_results


def main():
    path_inputs = '../instances/test_short.yml'
    inputs = CreateInputs(path_inputs)

    simulation = Simulate(
        inputs=inputs,
    )
    simulation.create_markets()
    market_results = simulation.run()
    plot_market_results(market_results)


if __name__ == "__main__":
    main()
