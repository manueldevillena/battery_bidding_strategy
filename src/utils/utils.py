import numpy as np
import numpy.typing as npt
import pandas as pd


def read_csv_file(fname: str, cols: list) -> pd.Series:
    """Reads csv file returning an array

    Parameters
    ----------
    fname : str
        path to csv file to read

    Returns
    -------
    pd.Series
    """
    df = pd.read_csv(fname, header=0, index_col=0).ffill()
    index_seconds = pd.date_range(start='2022-04-01 00:00:00', end='2022-04-30 23:59:59', freq='S')
    index_half_hours = pd.date_range(start='2022-04-01 00:00:00', end='2022-04-30 23:30:00', freq='30T')
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


def pivot_dataframe(df: pd.DataFrame, idx: str, cols: list[str]) -> pd.Series:
    """Pivots a dataframe to extract an indexed Series

    Parameters
    ----------
    df : pd.DataFrame
        dataframe to pivot
    idx : index
        index column
    cols : list
        columns to keep

    Returns
    -------
    series : pd.Series
        indexed series
    """
    return df.pivot(index=idx, columns=cols)
