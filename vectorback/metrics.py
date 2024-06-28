"""Defines metrics for evaluating strategies."""

from warnings import warn

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dataset import Dataset


def sharpe_ratio(
    returns: pd.Series | np.ndarray | list,
    target_return: pd.Series | np.ndarray | list | float = 0.0,
    period: str = "1d",
    window: int = -100,
) -> float:
    """Calculates Sharpe Ratio."""
    match type(returns):
        case pd.Series:
            returns = returns.values
        case list:
            returns = np.array(returns)

    warnstr = (
        "Sharpe Ratio calculation ({period}) has been provided data of length {length}. "
        + "This is less than the window size of {window}."
    )
    multiplier = 1.0

    match period:
        case "1d":
            # window is 252 days
            window = 252 if window == -100 else window
            multiplier = 252**0.5
            if len(returns) < window:
                warn(warnstr.format(period=period, length=len(returns), window=window))
        case "1w":
            # window is 52 weeks
            window = 52 if window == -100 else window
            multiplier = 52**0.5
            if len(returns) < window:
                warn(warnstr.format(period=period, length=len(returns), window=window))
        case "1m":
            # window is 12 months
            window = 12 if window == -100 else window
            multiplier = 12**0.5
            if len(returns) < window:
                warn(warnstr.format(period=period, length=len(returns), window=window))
        case "1y":
            # window is past 10 years
            window = 10 if window == -100 else window
            if len(returns) < window:
                warn(warnstr.format(period=period, length=len(returns), window=window))
        case _:
            raise ValueError(
                "Specified period for data is not valid. Use 1d, 1w, 1m, or 1y."
            )

    match type(target_return):
        case pd.Series:
            target_return = target_return.values
        case list:
            target_return = np.array(target_return)

    r = (returns - target_return).mean() / returns.std() * multiplier

    return r


def sortino_ratio(
    returns: pd.Series | np.ndarray | list,
    target_return: pd.Series | np.ndarray | list | float = 0.0,
    period: str = "1d",
    window: int = -100,
) -> float:
    """Calculates Sortino Ratio."""
    match type(returns):
        case pd.Series:
            returns = returns.values
        case list:
            returns = np.array(returns)

    warnstr = (
        "Sortino Ratio calculation ({period}) has been provided data of length {length}. "
        + "This is less than the window size of {window}."
    )
    multiplier = 1.0

    match period:
        case "1d":
            # window is 252 days
            window = 252 if window == -100 else window
            multiplier = 252**0.5
            if len(returns) < window:
                warn(warnstr.format(period=period, length=len(returns), window=window))
        case "1w":
            # window is 52 weeks
            window = 52 if window == -100 else window
            multiplier = 52**0.5
            if len(returns) < window:
                warn(warnstr.format(period=period, length=len(returns), window=window))
        case "1m":
            # window is 12 months
            window = 12 if window == -100 else window
            multiplier = 12**0.5
            if len(returns) < window:
                warn(warnstr.format(period=period, length=len(returns), window=window))
        case "1y":
            # window is past 10 years
            window = 10 if window == -100 else window
            if len(returns) < window:
                warn(warnstr.format(period=period, length=len(returns), window=window))
        case _:
            raise ValueError(
                "Specified period for data is not valid. Use 1d, 1w, 1m, or 1y."
            )

    match type(target_return):
        case pd.Series:
            target_return = target_return.values
        case list:
            target_return = np.array(target_return)

    r = (
        (returns - target_return).mean()
        / np.where(returns < 0, 0.0, returns).std()
        * multiplier
    )

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
    print(sortino_ratio(data.returns["NVDA"].values.tolist()))
    breakpoint()
