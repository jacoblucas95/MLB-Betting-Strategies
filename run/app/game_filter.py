#!/usr/bin/env python3
import os
import pandas as pd
from datetime import date
from app import fix_df_types

csvfile = os.path.join(os.path.dirname(__file__), '..', 'setup', 'data', 'baseball.csv')
df = pd.read_csv(csvfile, low_memory=False)
df = fix_df_types(df)

class Filter:
    
    def __init__(self, start_date, end_date, h_a, f_d):
        self.start_date = start_date
        self.end_date = end_date
        self.h_a = h_a
        self.f_d = f_d
        
    def get_df(self):
        df['date'] = pd.to_datetime(df['date'])
        df2 = df[df['date'].isin(pd.date_range(self.start_date,self.end_date))]
        if self.f_d == 'f':
            df2 = df.loc[(df['visitor_home'] == self.h_a) & (df['money_line_close'] < 0)]
        else:
            df2 = df.loc[(df['visitor_home'] == self.h_a) & (df['money_line_close'] > 0)]
        return df2

if __name__ == '__main__':
    print()
