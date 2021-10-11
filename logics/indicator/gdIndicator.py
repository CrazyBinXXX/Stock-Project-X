from logics.indicator import Indicator
import dataHouse.fetchData as fd
import numpy as np
import pandas as pd
from scipy import stats
from colorama import Fore
from colorama import Style
from matplotlib import pyplot as plt
import datetime as dt
import yfinance as yf

def softmax(t):
    return 1 / (1 + np.e**(-t))

# A class for gex and dix indicator
class GdIndicator(Indicator):
    def readData(self):
        self.dix_df = fd.getAllDf()
        self.gex_df = fd.getGEXdf()
        self.dix_arr = np.array(self.dix_df['dix'])
        self.gex_arr = np.array(self.gex_df['gex'])
        self.dix_mean = self.dix_arr.mean()
        self.dix_std = self.dix_arr.std()
        self.gex_mean = self.gex_arr.mean()
        self.gex_std = self.gex_arr.std()

    # This function will grade a trading date whether its
    # a good buy point based on dix and gex
    def rateADate(self, date):
        dix_arr = np.array(fd.getDIXbyDate(date)['dix'])
        gex_arr = np.array(fd.getGEXbyDate(date)['gex'])
        dix_score = np.round(softmax((dix_arr - self.dix_mean) / self.dix_std) * 100, 2)
        gex_score = 100 - np.round(softmax((gex_arr - self.gex_mean) / self.gex_std) * 100, 2)
        data = {'Date': date,
                'DIX Score': dix_score,
                'GEX Score': gex_score,
                'Comprehensive Score': dix_score * 0.4 + gex_score * 0.6}
        df = pd.DataFrame(data)
        # for idx, row in df.iterrows():
        #     if row['Comprehensive Score'] > 70:
        #         print(f'{Fore.RED}{row}{Style.RESET_ALL}')
        #     elif row['Comprehensive Score'] < 20:
        #         print(f'{Fore.GREEN}{row}{Style.RESET_ALL}')
        #     else:
        #         print(row)
        return df

if __name__ == '__main__':
    win = GdIndicator()
    win.readData()
    date_list = fd.getDate('2020-01-21', '2021-06-18')
    # print(date_list)
    result = win.rateADate(date_list)
    print(result.to_string())
    scores = np.array(result['Comprehensive Score'])
    plt.plot(scores)
    qqq = yf.Ticker('qqq').history(period='3000d')[['Close']]
    qqq.reset_index(level=0, inplace=True)
    qqq = qqq[qqq['Date'].isin(date_list)]
    print(qqq)
    y = np.array(qqq['Close'])
    plt.plot(y, color='red')
    plt.show()