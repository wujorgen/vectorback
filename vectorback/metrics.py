"""Defines metrics for evaluating strategies."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from dataset import Dataset


def sharpe_ratio(
    returns: pd.Series | np.ndarray | list,
    target_return: pd.Series | np.ndarray | list | float = 0.0,
    lookback: int = 250,
    period: str = "1d",
) -> float:
    if period not in ["1d", "1w", "1m"]:
        raise ValueError("Specified period for data is not valid. Use 1d, 1w, or 1m.")
    if type(returns) == pd.Series:
        returns = returns.values
    elif type(returns) == list:
        returns = np.array(list)
    r = returns.mean() / returns.std()
    match period:
        case "1d":
            r *= 250**0.5
        case "1w":
            r *= 50**0.5
        case "1m":
            r *= 12**0.5
    return r


def sortino_ratio(
    returns: pd.Series | np.ndarray | list,
    target_return: pd.Series | np.ndarray | list | float = 0.0,
    lookback: int = 250,
    period: str = "1d",
) -> float:
    if period not in ["1d", "1w", "1m"]:
        raise ValueError("Specified period for data is not valid. Use 1d, 1w, or 1m.")
    if type(returns) == pd.Series:
        returns = returns.values
    elif type(returns) == list:
        returns = np.array(list)
    r = returns.mean() / np.where(returns < 0, 0.0, returns).std()
    match period:
        case "1d":
            r *= 250**0.5
        case "1w":
            r *= 50**0.5
        case "1m":
            r *= 12**0.5
    return r


def calmar_ratio():
    pass


def drawdown(type: str = "max" or "min"):
    pass


def market_beta():
    pass


def market_alpha():
    pass


def value_at_risk():
    pass


def conditional_value_at_risk():
    pass


# TODO: does factor regression go here?

if __name__ == "__main__":
    tickers = ["NVDA", "CAT", "TSLA"]
    data = Dataset(tickers)
    weights = pd.DataFrame(np.ones((data.returns.shape[0], len(tickers))))
    weights.set_index(data.returns.index, inplace=True)
    print(data.prices)
    print(data.returns)
    print(sharpe_ratio(data.returns["NVDA"]))
    print(sortino_ratio(data.returns["NVDA"]))
    breakpoint()
