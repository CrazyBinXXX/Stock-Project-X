from logics.strat import Strategy
from collections import defaultdict

class SimuAccount:
    def __init__(self):
        self.simulator = None
        self.strategy = None
        self.cash = 0
        self.positions = defaultdict(lambda : 0)

    def initAccount(self, cash_amount, positions=None):
        self.cash = cash_amount
        self.positions = positions
        if not positions:
            self.positions = defaultdict(lambda: 0)

    def getCash(self):
        return self.cash

    def getPositions(self):
        return self.positions

    def printInfo(self):
        print(f'Our current cash: {self.cash}.')
        print(f'Our Current Positions: {self.positions}.')

    def seeDate(self):
        return self.simulator.getCurDate()

    # Return the price of the ticker at that date
    def seePrice(self, ticker):
        return self.simulator.lookupPrice(ticker)

    def getValue(self):
        v = self.cash
        if self.positions:
            for ticker, amount in self.positions.items():
                v += amount * self.seePrice(ticker)
        v = round(v, 2)
        return v

    # Buy a single ticker at one amount
    def buyTicker(self, ticker, amount):
        ticker_price = self.seePrice(ticker)
        actual_amount = min(amount, int(self.cash // ticker_price))
        self.cash -= actual_amount * ticker_price
        self.cash = round(self.cash, 2)
        self.positions[ticker] += actual_amount

    def buyTickerAll(self, ticker):
        ticker_price = self.seePrice(ticker)
        actual_amount = int(self.cash // ticker_price)
        self.cash -= actual_amount * ticker_price
        self.cash = round(self.cash, 2)
        self.positions[ticker] += actual_amount

    # Sell a single ticker at one amount
    def sellTicker(self, ticker, amount):
        ticker_price = self.seePrice(ticker)
        actual_amount = min(self.positions[ticker], amount)
        self.cash += actual_amount * ticker_price
        self.positions[ticker] -= actual_amount

    def sellTickerAll(self, ticker):
        ticker_price = self.seePrice(ticker)
        self.cash += self.positions[ticker] * ticker_price
        self.positions[ticker] = 0

    # A new day. Decide your move. You will want to ask your strategy
    def step(self):
        decision = self.strategy.step()
        pass