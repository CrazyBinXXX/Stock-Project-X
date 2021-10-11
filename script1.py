import yfinance as yf
from colorama import Fore, Style
import mplfinance as mpf

def pattern_recognizer(rows):
    row1 = rows[0]
    row2 = rows[1]
    row3 = rows[2]

if __name__ == '__main__':
    qqq = yf.Ticker('QQQ')
    hist = qqq.history(period="300d")
    hist = hist.round(2)
    dates = list(hist.index)
    for idx in range(hist.shape[0] - 2):
        # print(hist.iloc[idx])
        day1 = hist.iloc[idx]
        day2 = hist.iloc[idx + 1]
        day3 = hist.iloc[idx + 2]
        # print('Open: ', hist.iloc[idx]['Open'])
        # print('Close: ', hist.iloc[idx]['Close'])
        requirement1 = day1['Close'] > day1['Open'] and day2['Open'] > day2['Close'] and day3['Close'] > day3['Open']
        requirement2 = day2['Open'] < day1['Close'] and day2['Close'] > day1['Open'] and day3['Open'] > day2['Close'] and day3['Close'] > day2['Open']
        if requirement1 and requirement2:
            print(Fore.RED + 'The pattern FIND! The three rows are:' + Style.RESET_ALL)
            print(day1)
            print(day2)
            print(day3)
    # mpf.plot(hist, type='candle', mav=(5, 10, 20), volume=True)
    # mpf.plot()