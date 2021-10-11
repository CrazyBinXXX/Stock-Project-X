import dataHouse.fetchData as fd
import yfinance as yf

class Indicator:
    def __init__(self):
        self.qqq = yf.Ticker('QQQ')
        self.spy = yf.Ticker('SPY')

