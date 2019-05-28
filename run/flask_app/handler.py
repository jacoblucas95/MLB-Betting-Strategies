#!/usr/bin/env python3
import os
import pandas as pd
import numpy as np
    
pickle_path = os.path.join(os.path.dirname(__file__), '..', 'setup', 'data', 'dataset.pickle')
df = pd.read_pickle(pickle_path)

def fix_df_types(df):
    df.drop(['Unnamed: 0'], axis=1, inplace=True)
    df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)
    return df

def get_game_data(gameno, df=df):
    game_test = df['gameno'] == gameno
    game_rows = df[game_test]
    return game_rows.iloc[0]

def game_sequence(df):
#    print('\n\n\n\n\nLOG:\n\n\n', df, '\n\n\n\n')
    for index in range(df.shape[0]):
        yield df.iloc[index]

'''
if __name__ == "__main__":
    games1 = game_sequence(df)
    game2 = get_game_data(10)
    print(game2)
'''



