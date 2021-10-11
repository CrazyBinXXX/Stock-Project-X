import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
import seaborn as sns
from datetime import timedelta, date
import datetime
from itertools import *

if __name__ == '__main__':
    df = pd.read_csv('data.csv', sep='\s+', header=None, skiprows=0)

    print(df.head())