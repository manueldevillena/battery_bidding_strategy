import numpy as np
import numpy.typing as npt
import pandas as pd

from . import GenericInteraction


class FRRInteraction(GenericInteraction):
    """Firm frequency response market.
    """
    def __init__(self, freq_data: pd.Series, ref_price: float, service_curve: npt.NDArray[tuple[float, float]],
                 initial_soc: float, ssp: pd.Series) -> None:
        super().__init__(freq_data, ssp)
        self.reference_price = ref_price
        self.service_curve = service_curve
        self.initial_soc = initial_soc
        self.soc = initial_soc
        self.soc_list = [initial_soc]
        self.profit = 0.0

    def activate(self):
        activations = self._get_freq_activation(self.service_curve)
        rest_until = activations.index[0]
        for t in activations.index:
            if t < rest_until:
                print(f'resting until {rest_until}... :_(')
                continue
            if self.soc_bounds[0] <= self.soc <= self.soc_bounds[1]:
                self.soc += activations[t] / 3600
                self.profit += (np.abs(activations[t]) / 3600) * self.reference_price
                self.soc_list.append(self.soc)
                print(f'Coin!! cumulated profit = {self.profit} :)')
            else:
                print(f'Soc out of bounds: soc = {self.soc}')
                self.soc = self.initial_soc
                t_ssp = t.floor(freq='30T')#.strftime('%Y-%d-%m %H:%M:%S')
                self.profit += (self.soc - self.initial_soc) * self.ssp[t_ssp]
                rest_until = t + pd.Timedelta('30T')
