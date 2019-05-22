#!/usr/bin/env python3
import os
import pandas as pd
from datetime import date
from app import fix_df_types

csvfile = os.path.join(os.path.dirname(__file__), '..', 'setup', 'data', 'baseball.csv')
df = pd.read_csv(csvfile, low_memory=False)
df = fix_df_types(df)

def date_range(df=df, start_date=date(2018,1,1), end_date=date(2019,12,31)):
    df['date'] = pd.to_datetime(df['date'])
    df2 = df[df['date'].isin(pd.date_range(start_date,end_date))]
    return df2

def home_away(h_a, df=df):
    df2 = df.loc(df['visitor_home'] == h_a)
    return df2

def fav_dog(f_d, df=df):
    if f_d == 'f':
        df2 = df.loc(df['money_line_close'] < 0)
        return df2
    else:
        df2 = df.loc(df['money_line_close'] > 0)
        return df2


if __name__ == '__main__':
    print()
