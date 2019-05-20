import os
import sqlite3
from os.path import dirname
from datetime import date
import numpy as np
import pandas as pd
from app import df, get_game_data, game_sequence

class Game:
    # df is the master pandas DataFrame imported from the local csv file
    # game class represents all the attributes for a given game by ingesting two rows from the dataframe
    # def __init__(self, data=df, game_num=int()):
    def __init__(self, visitor_row, home_row):

        self.date = None
        self.opening_ou_line = visitor_row['']
        self.opening_over_odds = int()
        self.opening_under_odds = int()
        self.closing_ou_line = float()
        self.closing_over_odds = int()
        self.closing_under_odds = int()
        self.totalruns = int()
        self.run_dif_game = int()

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
    
    def money_line_bet(self, strategy_func):
        choice = strategy_func(self)
        if choice is None:
            return 0
        elif choice == self.winner():
            return 1
        else:
            return -1

    def winner(self):
        if self.home_run_dif_game > 0:
            return 'H'
        else:
            return 'V'
    
    
    def bet_payout(self, winner):
        if winner == 'H':
            pass
        #     return abs()/100
        # else:
        #     return 1 / (abs(odds)/100)

if __name__ == "__main__":
    for visitor_row, home_row in game_sequence():
        g = Game(visitor_row, home_row)
        print(g.winner())
        
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