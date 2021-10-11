from logics.strat import Strategy
from logics.indicator.gdIndicator import GdIndicator


class GdStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.name = 'gd'
        self.type = 'buySellPoints'
        self.indicator = GdIndicator()
        self.indicator.readData()
        self.account = None
        self.ticker = 'QQQ'
        self.lastDate = None

    # Our agent comes to a new day, the simulator will feed us everything
    def step(self):
        cur_date = self.seeDate()
        if self.lastDate:
            score = round(float(self.indicator.rateADate([self.lastDate])['Comprehensive Score']), 2)
        else:
            score = 50
        # print('Score in a past day: ')
        # print(score)
        # Our strategy: if score > 70, we buy all, if score < 20, we sell all
        if score > 70:
            self.account.buyTickerAll(self.ticker)
            # cash = self.account.getCash()
            # value = self.account.getValue()
            # position_value = value - cash
            # self.account.buyTicker(self.ticker, (cash / 2) // self.account.seePrice(self.ticker))
        elif score < 20:
            # self.account.sellTickerAll(self.ticker)
            self.account.sellTicker(self.ticker, self.account.getPositions()[self.ticker] // 3)
        else:
            pass
        self.lastDate = cur_date

if __name__ == '__main__':
    gs = GdStrategy()