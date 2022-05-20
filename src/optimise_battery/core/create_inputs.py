from dataclasses import dataclass, field

import pandas as pd

from utils import read_config, read_csv_file


@dataclass
class CreateInputs:
    """Dataclass with inputs for the simulation.
    """
    inputs_path: str
    config: dict = field(init=False)
    freq: pd.Series = field(init=False)
    ssp: pd.Series = field(init=False)
    markets: dict[dict[str, tuple | float | bool]] = field(init=False)
    learning_rate: float = field(init=False)

    def __post_init__(self):
        # Read config file
        self.config = read_config(self.inputs_path)

        # Create input data
        self.freq = read_csv_file(self.config['freq_data'], self.config['freq_column'], self.config['start_date'], self.config['end_date'])
        self.ssp = read_csv_file(self.config['ssp_data'], self.config['ssp_column'], self.config['start_date'], self.config['end_date'])
        self.learning_rate = self.config['learning_rate']
        self.markets = self.config['markets']
