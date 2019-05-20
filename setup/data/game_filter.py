#!/usr/bin/env python3

import pandas as pd
import datetime

df = pd.read_csv('baseball.csv', low_memory=False)

def date_range(df=df):
    df['date'] = pd.to_datetime(df['date'])
    df2 = df[df['date'].isin(pd.date_range('2010-04-05','2010-04-06'))]
    return df2

def home_underdogs(df=df):
    df2 = df.loc[(df['visitor_home'] == 'H') & (df['money_line_close'] > 0)]
    return df2

if __name__ == '__main__':
    print(home_underdogs())
