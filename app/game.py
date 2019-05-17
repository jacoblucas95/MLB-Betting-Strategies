import os
import sqlite3
from os.path import dirname
import numpy as np
import pandas as pd
from app import df

class Game:
    # df is the master pandas DataFrame imported from the local csv file
    # ['Unnamed: 0', '1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', 'close', 'close_ou', 'closeouodds', 'date', 'final', 'gameno', 'open', 'open_ou', 'openou', 'openouodds', 'pitcher', 'rot', 'rundif', 'runline', 'runlineodds', 'team', 'totalruns', 'vh', 'winrl', 'wintotal']
    # game class represents all the attributes for a given game by ingesting two rows from the dataframe
    def __init__(self, data=df, game_num=int()):
        home_team_row_series = data.loc[(data['gameno'] == game_num) & (data['vh'] == 'H')]
        away_team_row_series = data.loc[(data['gameno'] == game_num) & (data['vh'] == 'V')]
        self.date = home_team_row_series['date']
        self.totalruns_closing_line = home_team_row_series['close_ou']
        self.totalruns_home_odds = home_team_row_series['closeouodds']
        self.totalruns_away_odds = away_team_row_series['closeouodds']
        self.totalruns_final = home_team_row_series['totalruns']
        self.home_team = home_team_row_series['team']
        self.away_team = away_team_row_series['team']

# functions for filtering game list 
        
        # self.home_team =
        # self.away_team = 

    

    
if __name__ == "__main__":
    g = Game(game_num=0)
    print('Game Date = {}'.format(g.date))
    print('Over-Under Closing Line = {}'.format(g.totalruns_closing_line))
    print('Over-Under Total Runs Home Team Odds = {}'.format(g.totalruns_home_odds))
    print('Over-Under Total Runs Away Team Odds = {}'.format(g.totalruns_away_odds))
    print('Home Team = {}'.format(g.home_team))
    print('Away Team = {}'.format(g.away_team))


    
    # t = Test()
    # t.field1 = "something"
    # t.field2 = "silly"
    # t.save()
    # t.field2 = "different"
    # t.save()

    # objects = Test.select_many()
    # for obj in objects:
    #     print("pk = ", obj.pk, obj.field1, obj.field2)