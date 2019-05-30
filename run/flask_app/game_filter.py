#!/usr/bin/env python3
import os
import pandas as pd
from datetime import date

# from .handler import fix_df_types

pickle_path = os.path.join(os.path.dirname(__file__), '..', 'setup', 'data', 'unix_dataset.pickle')
df = pd.read_pickle(pickle_path)

class Filter:
    
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def date_range_df(self):
        day_early = 24*60*60
        sd = self.start_date - day_early
        ed = self.end_date
        df_new = df[df['date'].between(sd, ed, inclusive=True)]

        return df
        return df_new

'''
if __name__ == '__main__':
    f = Filter(date(2018, 1, 1), date.today())
    print(f.date_range_df())
'''
