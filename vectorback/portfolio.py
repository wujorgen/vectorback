import pandas as pd
from asset import Asset
from indicators import moving_average


class Portfolio:
    def __init__(self, initial_capital=10000):
        self._initial_capital = initial_capital
        self._cash = initial_capital
        self._assets = {}
        self._tickers = []
        self._weights = pd.DataFrame()
        self._shares = pd.DataFrame()
        self._transaction_history = []
        self._total_value_history = []

    @property
    def initial_capital(self):
        return self._initial_capital

    @property
    def cash(self):
        return self._cash

    @cash.setter
    def cash(self, amount):
        self._cash = amount

    @property
    def assets(self):
        return self._assets

    @property
    def weights(self):
        return self._weights

    @property
    def shares(self):
        return self._shares

    @property
    def transaction_history(self):
        return self._transaction_history

    @property
    def total_value_history(self):
        return self._total_value_history

    def trim_dates(self):
        """This function trims the dates of all asset data to match."""
        pass

    def add_asset(self, asset):
        self._assets[asset.ticker] = asset

    def buy(self, ticker, quantity, price):
        cost = quantity * price
        if cost > self._cash:
            raise ValueError("Not enough cash to buy.")
        self._cash -= cost
        if ticker in self._positions:
            self._positions[ticker] += quantity
        else:
            self._positions[ticker] = quantity
        self._transaction_history.append((ticker, "BUY", quantity, price))

    def sell(self, ticker, quantity, price):
        if ticker not in self._positions or self._positions[ticker] < quantity:
            raise ValueError("Not enough shares to sell.")
        revenue = quantity * price
        self._cash += revenue
        self._positions[ticker] -= quantity
        if self._positions[ticker] == 0:
            del self._positions[ticker]
        self._transaction_history.append((ticker, "SELL", quantity, price))

    def update_value(self):
        total_value = self._cash
        for ticker, quantity in self._positions.items():
            price = self._assets[ticker].price.iloc[-1]
            total_value += quantity * price
        self._total_value_history.append(total_value)
        return total_value

    def get_portfolio_value(self):
        return (
            self._total_value_history[-1]
            if self._total_value_history
            else self._initial_capital
        )


# Example usage
if __name__ == "__main__":
    # Create assets
    apple = Asset("AAPL")
    apple.data = ("2020-01-01", "2023-01-01")  # Load data using property setter
    apple.add_indicator("50_MA", moving_average, window=50)

    # Create a portfolio
    portfolio = Portfolio(initial_capital=100000)
    portfolio.add_asset(apple)

    # Simulate some trades
    portfolio.buy("AAPL", 10, apple.price.iloc[-1])
    portfolio.sell("AAPL", 5, apple.price.iloc[-1])

    # Update and get portfolio value
    portfolio_value = portfolio.update_value()
    print(f"Current Portfolio Value: {portfolio_value}")

    # Print transaction history
    print("Transaction History:", portfolio.transaction_history)
