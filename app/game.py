import os
import sqlite3
from os.path import dirname
from datetime import date
import numpy as np
import pandas as pd
from app import df


class Game:
    # df is the master pandas DataFrame imported from the local csv file
    # ['Unnamed: 0', '1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', 'close', 'close_ou', 'closeouodds', 'date', 'final', 'gameno', 'open', 'open_ou', 'openou', 'openouodds', 'pitcher', 'rot', 'rundif', 'runline', 'runlineodds', 'team', 'totalruns', 'vh', 'winrl', 'wintotal']
    # game class represents all the attributes for a given game by ingesting two rows from the dataframe
    # def __init__(self, data=df, game_num=int()):
    def __init__(self):
        self.date = None
        self.opening_ou_line = float()
        self.opening_over_odds = int()
        self.opening_under_odds = int()
        self.closing_ou_line = float()
        self.closing_over_odds = int()
        self.closing_under_odds = int()
        self.totalruns = int()

        self.home_team = None
        self.away_team = None
        self.money_line_fav_runs = None
        self.money_line_dog_runs = None
        self.opening_money_line_fav_team = None
        self.opening_money_line_dog_team = None
        self.closing_money_line_fav_team = None
        self.closing_money_line_dog_team = None
        self.opening_money_line_fav_line = None
        self.opening_money_line_dog_line = None
        self.closing_money_line_fav_line = None
        self.closing_money_line_dog_line = None
        self.opening_money_line_fav_odds = None
        self.opening_money_line_dog_odds = None
        self.closing_money_line_fav_odds = None
        self.closing_money_line_dog_odds = None
    
    
    def bet(self, bet_type):
        if bet_type == 'over':
            if self.totalruns > self.closing_ou_line:
                return 1
            elif self.totalruns < self.closing_ou_line:
                return -1
            else:
                return 0
        elif bet_type == 'under':
            if self.totalruns < self.closing_ou_line:
                return 1
            elif self.totalruns > self.closing_ou_line:
                return -1
            else:
                return 0
        elif bet_type == 'money_line_fav':
            if self.money_line_fav_runs > self.money_line_dog_runs:
                return 1
            else:
                return -1
        elif bet_type == 'money_line_dog':
            if self.money_line_fav_runs < self.money_line_dog_runs:
                return 1
            else:
                return -1
        else:
            raise TypeError('Invalid or no bet_type entered')        
    
    def bet_payout(self, odds):
        if odds > 0:
            return abs(odds)/100
        else:
            return 1 / (abs(odds)/100)

if __name__ == "__main__":
    g = Game()
    g.closing_over_odds = -110
    g.totalruns = 16
    g.closing_ou_line = 9
    x = g.bet('over') * g.bet_payout(g.closing_over_odds)
    print(x)
    print()
        
    # g = Game(game_num=0)
    # print('Game Date = {}'.format(g.date))
    # print('Over-Under Closing Line = {}'.format(g.totalruns_closing_line))
    # print('Over-Under Total Runs Home Team Odds = {}'.format(g.totalruns_home_odds))
    # print('Over-Under Total Runs Away Team Odds = {}'.format(g.totalruns_away_odds))
    # print('Home Team = {}'.format(g.home_team))
    # print('Away Team = {}'.format(g.away_team))


    
    # t = Test()
    # t.field1 = "something"
    # t.field2 = "silly"
    # t.save()
    # t.field2 = "different"
    # t.save()

    # objects = Test.select_many()
    # for obj in objects:
    #     print("pk = ", obj.pk, obj.field1, obj.field2)