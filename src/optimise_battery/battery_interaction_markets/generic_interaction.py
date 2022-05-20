import numpy.typing as npt
import pandas as pd

from abc import ABC, abstractmethod

from optimise_battery.curves import BiddingCurve
from utils import find_nearest


class GenericInteraction(ABC):
    """Market interface.
    """
    def __init__(
            self,
            freq_data: pd.Series,
            ssp: pd.Series,
            market_name: str,
            ref_price: float,
            bidding_curve: BiddingCurve
    ) -> None:

        self.freq_data = freq_data
        self.ssp = ssp
        self.market_name = market_name
        self.reference_price = ref_price
        self.bidding_curve = bidding_curve

    def __repr__(self):
        return f'{self.market_name}'

    @abstractmethod
    def activate(self, price_market: float = None) -> float:
        """Performs the balancing activation of the battery in the market

        Parameters
        ----------
        price_market : float
            reference price of the market to modify the starting one
        Returns
        -------
        profit : float
            total profit after interacting in this market
        """
        raise NotImplementedError

    def _create_bidding_curve(self) -> npt.NDArray[tuple[float, float]]:
        """Creates bidding curve of the battery for this market
        """
        return self.bidding_curve.create_curve()

    def _get_freq_activation(self, service_curve: npt.NDArray[tuple[float, float]]) -> pd.Series:
        """Matches a given frequency with the possible activation

        Parameters
        ----------
        service_curve : npt.NDArray
            curve of balancing service of the battery in the market
        Returns
        -------
        activations : pd.Series
            Series with the possible activations
        """
        activations = pd.Series(index=self.freq_data.index, dtype=float)
        for t in self.freq_data.index:
            freq = self._check_freq(t)
            idx = find_nearest(service_curve[:, 0], freq)
            activations[t] = service_curve[idx, 1]

        return activations

    def _check_freq(self, timestamp: pd.Timestamp) -> float:
        """Checks the frequency at a given point in time

        Parameters
        ----------
        timestamp : pd.Timestamp
            timestamp to check the frequency

        Returns
        -------
        freq : float
            frequency at the given timestamp
        """
        return self.freq_data[timestamp]
