import unittest
import yfinance as yf
import numpy as np
import pandas as pd
from logics.simulator import Simulator
from logics.simuAccount import SimuAccount
from logics.strat import Strategy
from logics.strat.gdStrat import GdStrategy
import matplotlib.pyplot as plt


class TestSimulator(unittest.TestCase):
    def testInitSettings(self):
        """
        Test the init function
        """
        simulator = Simulator()
        strategy = GdStrategy()
        account = SimuAccount()
        simulator.initSettings('2018-06-21', '2021-06-11', ['QQQ', 'SPY', 'DIA'], strategy, account, 5000, {'QQQ': 10})
        self.assertIn('QQQ', simulator.market_data.columns)
        self.assertIn('SPY', simulator.market_data.columns)
        self.assertIn('DIA', simulator.market_data.columns)
        print(simulator.market_data)
        self.assertEqual(6720.7, simulator.start_money)
        account.printInfo()
        # while True:
        #     try:
        #         print(next(simulator.date_iter))
        #     except StopIteration:
        #         print('STOP')
        #         break

    def testNormalReturn(self):
        simulator = Simulator()
        strategy = GdStrategy()
        account = SimuAccount()
        simulator.initSettings('2018-06-21', '2021-06-11', ['QQQ', 'SPY', 'DIA'], strategy, account, 5000, {'QQQ': 10})
        self.assertEqual(1.11, simulator.normalReturn('SPY', '2021-06-01', '2021-06-11'))

    def testStep(self):
        simulator = Simulator()
        strategy = GdStrategy()
        account = SimuAccount()
        simulator.initSettings('2018-06-21', '2018-06-25', ['QQQ', 'SPY', 'DIA'], strategy, account, 5000, {'QQQ': 10})
        # self.assertEqual('2018-06-21', simulator.cur_date)
        simulator.step()
        self.assertEqual('2018-06-22', simulator.cur_date)
        simulator.step()
        self.assertEqual('2018-06-25', simulator.cur_date)
        self.assertFalse(simulator.simulationStop)
        simulator.step()
        self.assertTrue(simulator.simulationStop)

    def testSimulate(self):
        simulator = Simulator()
        strategy = GdStrategy()
        account = SimuAccount()
        simulator.initSettings('2016-01-05', '2018-06-25', ['QQQ', 'SPY', 'DIA'], strategy, account, 5000, {'QQQ': 10})
        simulator.simulate()
        # print(simulator.money_array)
        spy = np.array(simulator.market_data['QQQ'])
        # plt.plot(simulator.money_array, color='green')
        # plt.plot(np.round(spy/spy[0]*simulator.start_money), color='red')
        # plt.axhline(y=simulator.start_money, color='blue')
        plt.plot(np.array(simulator.money_array) - np.array(spy[:-1]/spy[0]*simulator.start_money), color='green')
        plt.axhline(y=0, color='blue')
        plt.show()

class TestGdStrategy(unittest.TestCase):
    def testStep(self):
        simulator = Simulator()
        strategy = GdStrategy()
        account = SimuAccount()
        simulator.initSettings('2018-06-21', '2021-06-11', ['QQQ', 'SPY', 'DIA'], strategy, account, 5000, {'QQQ': 10})
        account.initAccount(5000)
        strategy.step()
        self.assertEqual(strategy.lastDate, '2018-06-21')

class TestAccount(unittest.TestCase):
    def testSeePrice(self):
        simulator = Simulator()
        strategy = GdStrategy()
        account = SimuAccount()
        simulator.initSettings('2020-01-04', '2021-06-11', ['QQQ', 'SPY', 'DIA'], strategy, account, 5000, {'QQQ': 10})
        price = account.seePrice('QQQ')
        self.assertEqual(172.26, round(price, 2))

    def testBuyTicker(self):
        simulator = Simulator()
        strategy = GdStrategy()
        account = SimuAccount()
        simulator.initSettings('2018-06-21', '2021-06-11', ['QQQ', 'SPY', 'DIA'], strategy, account, 5000, {'QQQ': 10})
        account.initAccount(5000)
        account.buyTicker('QQQ', 10)
        print(account.positions)
        self.assertEqual(3277.4, round(account.cash, 2))

    def testSellTicker(self):
        simulator = Simulator()
        strategy = GdStrategy()
        account = SimuAccount()
        simulator.initSettings('2018-06-21', '2021-06-11', ['QQQ', 'SPY', 'DIA'], strategy, account, 5000, {'QQQ': 10})
        account.initAccount(5000)
        account.buyTicker('QQQ', 10)
        account.sellTicker('QQQ', 5)
        self.assertEqual(4138.7, round(account.cash, 2))
        self.assertEqual(5, account.positions['QQQ'])

if __name__ == '__main__':
    unittest.main()