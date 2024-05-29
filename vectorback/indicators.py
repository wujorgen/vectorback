import numpy as np
import pandas as pd


def moving_average(values: pd.Series, window: int):
    return values.rolling(window=window).mean()
