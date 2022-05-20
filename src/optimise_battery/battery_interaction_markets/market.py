import numpy as np
import numpy.typing as npt
import pandas as pd

from . import GenericInteraction
from optimise_battery.curves import BiddingCurve


class Market(GenericInteraction):
    """Firm frequency response market.
    """
    def __init__(
            self,
            freq_data: pd.Series,
            ssp: pd.Series,
            market_name: str,
            ref_price: float,
            bidding_curve: BiddingCurve,
            capacity: float = 8.0,
            soc_bounds: tuple = (0.25, 0.75)
    ) -> None:
        """

        Parameters
        ----------
        """

        # Market environment
        super().__init__(freq_data, ssp, market_name, ref_price, bidding_curve)

        # Battery parameters
        self.capacity = capacity
        self.soc_bounds = tuple(x * capacity for x in soc_bounds)
        self.initial_soc = capacity / 2
        self.soc = capacity / 2
        self.soc_list = [self.soc]

    def activate(self, price_market: float = None) -> tuple[float, list[float]]:
        if price_market is not None:
            self.reference_price = price_market

        bidding_curve = self._create_bidding_curve()
        profit = 0.0
        profit_list = [profit]
        activations = self._get_freq_activation(bidding_curve)
        rest_until = activations.index[0]
        for t in activations.index:
            if t < rest_until:
                print(f'resting until {rest_until}... :_(')
                continue
            if self.soc_bounds[0] <= self.soc <= self.soc_bounds[1]:
                self.soc += activations[t] / 3600
                profit += (np.abs(activations[t]) / 3600) * self.reference_price
                self.soc_list.append(self.soc)
                print(f'Coin!! cumulated profit = {profit} :)')
                profit_list.append(profit)
            else:
                print(f'Soc out of bounds: soc = {self.soc}')
                self.soc = self.initial_soc
                t_ssp = t.floor(freq='30T')
                profit += (self.soc - self.initial_soc) * self.ssp[t_ssp]
                rest_until = t + pd.Timedelta('30T')
                profit_list.append(profit)

        return profit, profit_list
