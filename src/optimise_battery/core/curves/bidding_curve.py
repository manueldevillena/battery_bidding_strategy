import numpy as np
import numpy.typing as npt

from dataclasses import dataclass


@dataclass
class BiddingCurve:
    """Describes the curve of service of the battery in the market
    """
    max_power: float
    affine_points_x: list[float]
    affine_points_y: list[float]
    min_power: float = 0.0
    base_freq: float = 50.0
    resolution_curve: int = 1000

    def create_curve(self) -> npt.NDArray:
        """Creates discrete function of x, y pairs following the required market curve

        Returns
        -------
        list : list with x, y pairs
        """
        curve_pairs = []
        for i in range(len(self.affine_points_x) - 1):
            x_coord = [self.affine_points_x[i], self.affine_points_x[i+1]]
            y_coord = [self.affine_points_y[i], self.affine_points_y[i+1]]

            coefficients = np.polyfit(x_coord, y_coord, deg=1)
            polynomial = np.poly1d(coefficients)

            x_values = np.linspace(x_coord[0], x_coord[1], self.resolution_curve)
            y_values = polynomial(x_values)

            curve_pairs.extend(zip(x_values + self.base_freq, y_values))

        curve_pairs.extend([(100-x, -y) for x, y in curve_pairs[:-1]][::-1])

        return np.array(curve_pairs)
