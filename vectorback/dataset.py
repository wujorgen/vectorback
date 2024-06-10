"""Defines the dataset class."""

import numpy as np
import pandas as pd
import yfinance as yf


class Dataset:
    """The Dataset class is a shitty wrapper around yfinance and pandas."""

    def __init__(
        self,
        tickers: list,
        start_date: pd.Timestamp = pd.Timestamp("2000-01-01"),
        end_date: pd.Timestamp = None,
    ) -> None:
        self.tickers = tickers
        self._dates = (start_date, end_date)
        self._rawdata = self.get_raw_data()
        self.data = self.process_data()

    @property
    def dates(self) -> tuple[pd.Timestamp]:
        return self.data.index[0], self.data.index[1]

    @property
    def prices(self) -> pd.DataFrame:
        return self.data["price"]

    @property
    def returns(self) -> pd.DataFrame:
        return self.data["returns"]

    def get_raw_data(self) -> dict[pd.DataFrame]:
        dct = dict.fromkeys(self.tickers)
        for ticker in self.tickers:
            print(ticker)
            dct[ticker] = yf.download(ticker, start=self._dates[0], end=self._dates[1])
        return dct

    def process_data(self) -> dict[pd.DataFrame]:
        df1 = pd.DataFrame()
        df2 = pd.DataFrame()
        for ticker in self.tickers:
            df1[f"{ticker}"] = self._rawdata[ticker]["Adj Close"]
            pcts = self._rawdata[ticker]["Adj Close"].pct_change()
            pcts.iloc[0] = 0.0
            df2[f"{ticker}"] = pcts
        df1.dropna(inplace=True)
        df2.dropna(inplace=True)
        for cdx in range(len(df2.columns.values)):
            df2.iloc[0, cdx] = 0.0
        return {"price": df1, "returns": df2}


if __name__ == "__main__":
    tickers = ["NVDA", "CAT", "TSLA"]
    data = Dataset(tickers)
    print(data.data)
    breakpoint()
