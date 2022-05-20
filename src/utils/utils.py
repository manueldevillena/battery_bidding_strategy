import numpy as np
import numpy.typing as npt
import pandas as pd

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def read_config(inputs_path: str) -> dict:
    """Reads YML file with inputs

    Parameters
    ----------
    inputs_path : str
        Path to the inputs file.

    Returns
    -------
    data : dict
        Dictionary with the read data.
    """
    with open(inputs_path) as infile:
        data = yaml.load(infile, Loader=Loader)
    return data


def read_csv_file(fname: str, cols: list, date_start: str, date_end: str) -> pd.Series:
    """Reads csv file returning an array

    Parameters
    ----------

    fname : str
        path to csv file to read
    cols : list[str]
        list of columns to read
    date_start : str
        date start for the time series
    date_end : str
        date end for the time series

    Returns
    -------
    series : pd.Series
        time series with required information
    """
    floored_date_end = str(pd.Timestamp(date_end).floor('30T'))
    index_seconds = pd.date_range(start=date_start, end=date_end, freq='S')
    index_half_hours = pd.date_range(start=date_start, end=floored_date_end, freq='30T')

    df = pd.read_csv(fname, header=0, index_col=0).ffill()
    values = df[cols].values.reshape(-1)
    if len(values) == len(index_seconds):
        series = pd.Series(index=index_seconds, data=values)
    elif len(values) == len(index_half_hours):
        series = pd.Series(index=index_half_hours, data=values)
    else:
        raise IndexError(f'The length of the index is incorrect. It should be {len(index_seconds)} or '
                         f'{len(index_half_hours)}, and it {len(values)}')

    return series


def find_nearest(array: npt.NDArray, value: float) -> int:
    """Finds the index of the nearest element to a given value in an array

    Parameters
    ----------
    array: npt.NDArray
        array in which to look for the nearest value
    value: float
        value to find in the array

    Returns
    -------
    int
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()

    return idx
