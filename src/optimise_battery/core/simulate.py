import numpy as np
import numpy.typing as npt

from dataclasses import dataclass, field

import pandas as pd

from optimise_battery.core import CreateInputs
from optimise_battery.curves import BiddingCurve
from optimise_battery.battery_interaction_markets import GenericInteraction, Market


EPS = 1e-3


@dataclass
class Simulate:
    """Simulates the bidding process of a battery in different balancing markets
    """
    inputs: CreateInputs
    benchmark_market: GenericInteraction = field(init=False)
    competing_markets: list[GenericInteraction] = field(init=False)
    initial_price: float = field(init=False)

    def create_markets(self):
        """Creates the list of markets
        """
        self.competing_markets = []
        for name, values in self.inputs.markets.items():
            if values['benchmark']:
                self.benchmark_market = self._create_market(
                    freq=self.inputs.freq,
                    ssp=self.inputs.ssp,
                    name=name,
                    values=values
                )
            else:
                self.competing_markets.append(
                    self._create_market(
                        freq=self.inputs.freq,
                        ssp=self.inputs.ssp,
                        name=name,
                        values=values
                    )
                )

    def run(self) -> float | dict[str, dict[str, float | npt.NDArray]]:
        """Runs the simulation
        """
        benchmark_profit, benchmark_profit_list = self.benchmark_market.activate()
        market_results = {}
        if not self.competing_markets:
            return benchmark_profit

        for market in self.competing_markets:
            profit = 0.0
            price_iteration = market.reference_price
            price_competing_market = [price_iteration]
            while (profit - benchmark_profit) < EPS:
                print('HERE', np.abs(profit - benchmark_profit))
                price_iteration = price_competing_market[-1]
                profit, profit_list = market.activate(price_iteration)
                price_competing_market.append(price_iteration * (1 + self.inputs.learning_rate))
                print('HERE2', price_iteration)

            market_results[market.market_name] = {
                'benchmark_profit': benchmark_profit,
                'total_profit': profit,
                'price_competing_market': np.array(price_competing_market),
                'break_even_price': price_iteration,
                'learning_rate': self.inputs.learning_rate
            }

        return market_results

    @staticmethod
    def _create_market(freq: pd.Series, ssp: pd. Series, name: str, values: dict) -> Market:
        """Creates one instance of a market

        Parameters
        ----------
        freq : pd.Series
        ssp : pd.Series
        name : str
        values : dict

        Returns
        -------
        market : Market
            market instance
        """
        return Market(
            freq_data=freq,
            ssp=ssp,
            market_name=name,
            ref_price=values['ref_price'],
            bidding_curve=BiddingCurve(values['affine_x'], values['affine_y'], max_power=values['max_power']),
            capacity=values['capacity']
        )
