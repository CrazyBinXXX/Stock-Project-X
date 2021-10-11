# This is a file that contains all functions used to fetch data
# includes stock price, gamma, gex, dix etc.
import pandas as pd
import yfinance as yf
import os

data_path = os.path.join(os.path.dirname(__file__), 'DIX.csv')
all_df = pd.read_csv(data_path)

def getAllDf():
    return all_df

def getDIXDf():
    dix_df = all_df[['date', 'dix']]
    return dix_df

def getGEXdf():
    gex_df = all_df[['date', 'gex']]
    return gex_df

def getDate(start_date, end_date):
    date_df = all_df['date']
    ret = []
    for idx in range(date_df.shape[0]):
        date = date_df.iloc[idx]
        if date >= start_date:
            ret.append(date)
        if date >= end_date:
            break
    return ret

# Date must be in format! It should be an iterable of date
def getDIXbyDate(date):
    dix_df = all_df[['date', 'dix']]
    rowbydate = dix_df.loc[dix_df['date'].isin(date)]
    return rowbydate

def getGEXbyDate(date):
    gex_df = all_df[['date', 'gex']]
    # print(gex_df)
    rowbydate = gex_df.loc[gex_df['date'].isin(date)]
    return rowbydate

# print(getDate('2021-05-06', '2021-05-13'))
# print(getAllDf().head(100))
# print(getGEXbyDate(['2021-06-17', '2021-06-18']))
