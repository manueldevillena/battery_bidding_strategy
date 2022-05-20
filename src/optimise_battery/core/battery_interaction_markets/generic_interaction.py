import numpy.typing as npt
import pandas as pd

from abc import ABC, abstractmethod

from utils import find_nearest


class GenericInteraction(ABC):
    """Market interface.
    """
    def __init__(self, freq_data: pd.Series, ssp: pd.Series, capacity: float = 8.0, soc_bounds: tuple = (0.25, 0.75)
                 ) -> None:
        self.freq_data = freq_data
        self.ssp = ssp
        self.capacity = capacity
        self.soc_bounds = tuple(x * capacity for x in soc_bounds)

    @abstractmethod
    def activate(self) -> None:
        """Performs the balancing activation of the battery in the market

        Returns
        -------
        None
        """
        raise NotImplementedError

    def _get_freq_activation(self, service_curve: npt.NDArray[tuple[float, float]]) -> pd.Series:
        """Matches a given frequency with the possible activation.

        Parameters
        ----------
        service_curve : npt.NDArray
            curve of balancing service of the battery in the market
        Returns
        -------
        activations : pd.Series
            Series with the possible activations.
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
