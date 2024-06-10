from abc import ABC

import pandas as pd
import yfinance as yf
from indicators import moving_average


class Asset(ABC):
    """Abstract class for all assets."""

    def __init__(self, symbol):
        self.symbol = symbol
        self.data = pd.DataFrame()
        self.indicators = {}

    def add_indicator(self, name, indicator_func, *args, **kwargs):
        self.indicators[name] = indicator_func(self.price, *args, **kwargs)

    def get_indicator(self, name):
        return self.indicators.get(name, None)


class Equity(Asset):
    """Equity class. Inherits Asset Abstract Base Class."""

    def __init__(self, symbol):
        self.symbol = symbol
        self.data = pd.DataFrame()
        self.weight = pd.DataFrame()
        self.indicators = {}

    @property
    def price(self):
        return self.data["Adj Close"]

    @property
    def pct(self):
        pct = self.price.pct_change()
        pct.iloc[0] = 0
        return pct * 100.0

    def load_data(self, start_date=None, end_date=None, per="1d"):
        self.data = yf.download(self.symbol, start=start_date, end=end_date, period=per)

    def add_indicator(self, name, indicator_func, *args, **kwargs):
        # self._indicators[name] = indicator_func(self.price, *args, **kwargs)
        super().add_indicator(name, indicator_func, *args, **kwargs)

    def get_indicator(self, name):
        # return self._indicators.get(name, None)
        return super().get_indicator(name)


# Example usage
if __name__ == "__main__":
    # Create an asset
    apple = Equity("AAPL")
    apple.load_data(start_date="2000-01-01", end_date="2023-01-01")
    apple.add_indicator("50_MA", moving_average, window=50)

    # Print data and indicator
    print(apple.data.head())
    print(apple.price.head())
    print(apple.get_indicator("50_MA").head())
    print(apple.data.tail())
    print(apple.price.tail())
    print(apple.get_indicator("50_MA").tail())
    breakpoint()
