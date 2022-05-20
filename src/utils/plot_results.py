import numpy as np
import matplotlib.pyplot as plt


def plot_market_results(market_results: dict) -> None:
    """Plots the market results

    Parameters
    ----------
    market_results

    Returns
    -------

    """
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(6, 4))
    for market, vals in market_results.items():
        x_values = np.array(range(len(vals['price_competing_market'])))
        y_values = np.array(vals['price_competing_market'])
        axes.plot(x_values, y_values, label=market)
        plt.legend()
    fig.savefig('market_results.pdf')
