import os
import pandas as pd
import numpy as np

csvfile = os.path.join(os.path.dirname(os.getcwd()), 'setup', 'data', 'baseball.csv')
df = pd.read_csv(csvfile, low_memory=False)
df.drop(['Unnamed: 0'], axis=1, inplace=True)
df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)

# df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)
# df.set_index('date', inplace=True)

def get_game_data(gameno, df=df):
    game_test = df['gameno'] == gameno
    game_rows = df[game_test]
    if len(game_rows) == 2:
        return game_rows.iloc[0], game_rows.iloc[1]
    return None

def game_sequence(df=df):
    for index in range(0, df.shape[0], 2):
        yield df.iloc[index], df.iloc[index+1]

if __name__ == "__main__":
    print(get_game_data(2))
            

