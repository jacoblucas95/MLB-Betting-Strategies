#!/usr/bin/env python3
import os
import pandas as pd
from datetime import date

from .handler import fix_df_types

csvfile = os.path.join(os.path.dirname(__file__), '..', 'setup', 'data', 'baseball.csv')
df = pd.read_csv(csvfile, low_memory=False)
df = fix_df_types(df)

class Filter:
    
    def __init__(self, start_date, end_date, visitor_home, favorite_underdog):
        self.start_date = start_date
        self.end_date = end_date
        self.visitor_home = visitor_home
        self.favorite_underdog = favorite_underdog
        self.df = df

    def get_df(self):
        self.df['date'] = pd.to_datetime(self.df['date'])
        df2 = self.df[self.df['date'].isin(pd.date_range(self.start_date, self.end_date))]
        if self.favorite_underdog == 'fav':
            df2 = df2.loc[(df2['visitor_home'] == self.visitor_home) & (df2['money_line_close'] < 0)]
        else:
            df2 = df2.loc[(df2['visitor_home'] == self.visitor_home) & (df2['money_line_close'] > 0)]
        return df2

if __name__ == '__main__':
    f = Filter(date(2018, 1, 1), date.today(), 'H', 'fav')
    print(f.get_df())