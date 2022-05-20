import matplotlib.pyplot as plt
import numpy as np

from .core.curves import BiddingCurve
from .core.battery_interaction_markets import FRRInteraction
from utils import read_csv_file, pivot_dataframe


if __name__ == "__main__":
    # Inputs
    file_freq_path = '../data/April_frequency.csv'
    file_data_path = '../data/Data.csv'
    freq = read_csv_file(file_freq_path, cols=['localFrequency'])
    ssp = read_csv_file(file_data_path, cols=['SSP [GBP/MWh]'])

    # Process
    # freq.plot()
    # plt.show()

    curve = BiddingCurve(
        max_power=10.0,
        affine_points_x=[-0.5, 0.0],
        affine_points_y=[10.0, 0.0]
    )
    curve_values = curve.create_curve()
    market = FRRInteraction(
        freq_data=freq,
        ref_price=10.0,
        service_curve=curve_values,
        initial_soc=4.0,
        ssp=ssp
    )
    market.activate()
    print(market.soc_list)
    print(market.profit / 1e3)

    plt.plot(range(len(market.soc_list)), market.soc_list)
    plt.show()

    # Do
