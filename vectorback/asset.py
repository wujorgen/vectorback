import pandas as pd
import yfinance as yf
from indicators import moving_average


class Asset:
    def __init__(self, ticker):
        self._ticker = ticker
        self._data = pd.DataFrame()
        self._price = pd.Series()
        self._pct = pd.Series()
        self._indicators = {}

    @property
    def ticker(self) -> str:
        return self._ticker

    @property
    def data(self) -> pd.DataFrame:
        return self._data

    @property
    def price(self) -> pd.Series:
        return self._price

    @property
    def pct(self) -> pd.Series:
        return self._pct

    @data.setter
    def data(self, date_range):
        start_date, end_date = date_range
        self._data = yf.download(self._ticker, start=start_date, end=end_date)
        self.price = self.data["Adj Close"]
        self.pct = self.price.pct_change()

    @price.setter
    def price(self, closing_prices):
        self._price = closing_prices

    @pct.setter
    def pct(self, pct_change):
        self._pct = pct_change
        self._pct.iloc[0] = 0
        self._pct *= 100

    def add_indicator(self, name, indicator_func, *args, **kwargs):
        self._indicators[name] = indicator_func(self.price, *args, **kwargs)

    def get_indicator(self, name):
        return self._indicators.get(name, None)


# Example usage
if __name__ == "__main__":
    # Create an asset
    apple = Asset("AAPL")
    apple.data = ("2020-01-01", "2023-01-01")  # Load data using property setter
    apple.add_indicator("50_MA", moving_average, window=50)

    # Print data and indicator
    print(apple.data.head())
    print(apple.price.head())
    print(apple.get_indicator("50_MA").head())
    print(apple.data.tail())
    print(apple.price.tail())
    print(apple.get_indicator("50_MA").tail())
    breakpoint()
