import yfinance as yf
import dataHouse.fetchData as fd
from logics.strat import Strategy
from logics.indicator.gdIndicator import GdIndicator
from logics.strat.gdStrat import GdStrategy
from logics.simuAccount import SimuAccount
import pandas as pd
import numpy as np


class Simulator:
    # We want our simulator could get market data and test our strat based on past data.
    # You could test with buy/sell date, buy/sell point, or strat.
    def __init__(self):
        self.start_date = ''
        self.end_date = ''
        self.strategy = None
        self.market_data = pd.DataFrame()
        self.date_iter = None
        self.cur_date = None
        self.simulationStop = False
        self.start_money = 0
        self.money_array = []

    def bind(self, strategy: Strategy, account: SimuAccount):
        self.strategy = strategy
        strategy.account = account
        account.simulator = self

    def initSettings(self, start_date, end_date, ticker_names, strategy: Strategy, account: SimuAccount,
                     start_cash, start_positions=None):
        self.start_date = start_date
        self.end_date = end_date
        self.market_data = pd.DataFrame()
        for ticker in ticker_names:
            ticker_data = yf.Ticker(ticker).history(period='3000d')
            self.market_data[ticker] = ticker_data['Close']
        self.market_data = self.market_data.loc[self.market_data.index >= start_date]
        self.market_data = self.market_data.loc[self.market_data.index <= end_date]
        self.market_data = self.market_data.round(2)
        self.date_iter = iter(fd.getDate(self.start_date, self.end_date))
        self.cur_date = next(self.date_iter)
        self.bind(strategy, account)
        self.strategy.account.initAccount(start_cash, start_positions)
        self.start_money = start_cash
        if start_positions:
            for ticker, amount in start_positions.items():
                self.start_money += amount * self.lookupPrice(ticker)
        self.money_array = []

    def getCurDate(self):
        return self.cur_date

    def lookupPrice(self, ticker):
        return self.market_data[ticker][self.cur_date]

    # Move to next day and tell the account
    def step(self):
        try:
            self.cur_date = next(self.date_iter)
            # Tell the account(user) it's the next day
            self.strategy.step()
            money = self.strategy.account.getCash()
            if self.strategy.account.getPositions():
                for ticker, amount in self.strategy.account.getPositions().items():
                    money += amount * self.lookupPrice(ticker)
            self.money_array.append(money)
        except StopIteration:
            self.simulationStop = True

    def printReport(self):
        start_money = round(self.start_money, 2)
        end_money = self.strategy.account.getCash()
        for ticker, amount in self.strategy.account.getPositions().items():
            end_money += amount * self.lookupPrice(ticker)
        end_money = round(end_money, 2)
        normal_return = self.normalReturn('QQQ', self.start_date, self.end_date)
        print(f'Out start money is: {start_money}.')
        print(f'Our end money is: {end_money}.')
        print(f'The return is {round((end_money / start_money - 1) * 100, 2)}%')
        print(f'The normal return is {normal_return}%.')

    # We start simulation! This function will start simulating buy & sell based on given
    # strategy. And return the result simuAccount.
    def simulate(self):
        # days go on ......
        while not self.simulationStop:
            self.step()
        # inspect our final return
        self.printReport()

    def normalReturn(self, ticker, buy_date, sell_date):
        buy_price = self.market_data[ticker][buy_date]
        sell_price = self.market_data[ticker][sell_date]
        ret = round((sell_price / buy_price - 1) * 100, 2)
        # print(buy_price, sell_price)
        return ret

    def nDaysReturn(self, n, ticker_name, buy_dates):
        ticker = yf.Ticker(ticker_name)
        ticker_data = ticker.history(period='3000d')[['Close']]
        ticker_data.reset_index(level=0, inplace=True)
        ret = []
        ticker_data['Diff n'] = ticker_data['Close'].shift(-n) - ticker_data['Close']
        ticker_data['Percent Change'] = round(ticker_data['Diff n'] / ticker_data['Close'] * 100, 2)
        result = ticker_data[ticker_data['Date'].isin(buy_dates)]
        return result[['Date', 'Diff n', 'Percent Change']]

if __name__ == '__main__':
    s = Simulator()
    buy_dates = []
    win = GdIndicator()
    win.readData()
    date_list = fd.getDate('2018-06-21', '2021-06-11')
    winrate = win.rateADate(date_list)
    winrate = winrate.loc[winrate['Comprehensive Score'] > 70]
    # print(winrate)
    buy_dates = np.array(winrate['Date'])
    ret = s.nDaysReturn(20, 'SPY', buy_dates)
    ret['Date'] = ret['Date'].astype(str)
    # print(ret)
    result = pd.merge(winrate, ret, left_on='Date', right_on='Date', how='inner').drop(['DIX Score', 'GEX Score'], axis=1)
    print(result.to_string())

