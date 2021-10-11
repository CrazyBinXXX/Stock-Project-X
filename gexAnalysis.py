import pandas as pd
import yfinance as yf
import mplfinance as mpf
from matplotlib import pyplot as plt
from scipy import stats
import numpy as np

def abline(slope, intercept):
    """Plot a line from slope and intercept"""
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, '--', c = 'green')

if __name__ == '__main__':
    df = pd.read_csv('DIX.csv')
    qqq = yf.Ticker('QQQ')
    hist = qqq.history(period="3000d")
    cnt = 0
    win = 0
    lose = 0
    interval = 30
    xaxis = []
    yaxis = []
    rois = []
    for idx in range(df.shape[0] - 2):
        row = df.iloc[idx]
        gex = row['gex']
        next_gex = df.iloc[idx+1]['gex']
        next_next_gex = df.iloc[idx+2]['gex']
        dix = row['dix']
        if dix > 0.44:
            print('Very low gex found!!!')
            date = row['date']
            price = hist.loc[df.iloc[idx+1]['date']]['Open']
            print('The date is', date)
            print('QQQ price is: ', price)
            if idx < df.shape[0] - interval:
                print('RETURN ANALYSIS')
                date_after_month = df.iloc[idx + interval]['date']
                print('Date is: ', date_after_month)
                price_after_month = hist.loc[date_after_month]['Close']
                print('QQQ price after is: ', price_after_month)
                print('Percent change: ')
                roi = price_after_month / price
                roi = (roi - 1) * 100
                print(roi, '%')
                print()
                if roi > 3:
                    win += 1
                if roi < 0:
                    lose += 1
                xaxis.append(dix)
                yaxis.append(gex)
                rois.append(roi)
            cnt += 1
    print()
    print('Win rate is: ', win, '/', cnt)
    print(round(win / cnt * 100, 2), '%')
    print('Lose rate is: ', lose, '/', cnt)
    print(round(lose / cnt * 100, 2), '%')
    # mpf.plot(hist, type='line', mav=(5, 10, 20), volume=True)
    # xaxis = np.array(xaxis)
    # yaxis = np.array(yaxis) / 1e10
    # rois = np.array(rois)
    # slope, intercept, r_value, p_value, std_err = stats.linregress(xaxis, yaxis)
    # print('Slope and p_value: ', slope, p_value)
    # plt.scatter(xaxis, yaxis, c = rois / np.linalg.norm(rois) * 10, s = 1)
    # abline(slope, intercept)
    # plt.xlabel('DIX')
    # plt.ylabel('GEX')
    # plt.gray()
    # plt.show()