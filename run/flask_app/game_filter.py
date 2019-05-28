#!/usr/bin/env python3
import os
import pandas as pd
from datetime import date

# from .handler import fix_df_types

pickle_path = os.path.join(os.path.dirname(__file__), '..', 'setup', 'data', 'dataset.pickle')
df = pd.read_pickle(pickle_path)

class Filter:
    
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def date_range_df(self):
        df['date'] = pd.to_datetime(df['date'])
        df_new = df[df['date'].isin(pd.date_range(self.start_date, self.end_date))]
        return df_new

'''
if __name__ == '__main__':
    f = Filter(date(2018, 1, 1), date.today())
    print(f.date_range_df())
'''
