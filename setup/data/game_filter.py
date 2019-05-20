#!/usr/bin/env python3

import pandas as pd
from datetime import date

df = pd.read_csv('baseball.csv', low_memory=False)

def date_range(df=df):
    y1 = int(input('start yr: '))
    m1 = int(input('start mon: '))
    d1 = int(input('start day: '))

    y2 = int(input('end yr: '))
    m2 = int(input('end mon: '))
    d2 = int(input('end day: '))

    start = date(y1,m1,d1)
    end = date(y2,m2,d2)
    df['date'] = pd.to_datetime(df['date'])
    df2 = df[df['date'].isin(pd.date_range(start,end))]
    return df2

def home_underdogs(df=df):
    df2 = df.loc[(df['visitor_home'] == 'H') & (df['money_line_close'] > 0)]
    return df2

if __name__ == '__main__':
    print(date_range())
