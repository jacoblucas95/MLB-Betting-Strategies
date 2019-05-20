import os
import sqlite3
from os.path import dirname
from datetime import date
import numpy as np
import pandas as pd
from app import df, get_game_data, game_sequence
from strategies import home_team

class Game:
    # df is the master pandas DataFrame imported from the local csv file
    # game class represents all the attributes for a given game by ingesting two rows from the dataframe
    # def __init__(self, data=df, game_num=int()):
    # ['gameno', 'team', 'visitor_home', 'team_run_total', 'total_runs_game',
    #    'money_line_close', 'money_line_open', 'over_under_line_close',
    #    'over_under_line_open', 'over_under_odds_close', 'over_under_odds_open',
    #    'pitcher', 'rot', 'run_dif_game', 'run_line_close',
    #    'run_line_odds_close']
    def __init__(self, visitor_row, home_row):
        self.date = visitor_row.date
        self.gameno = visitor_row.gameno
        self.total_runs_game = visitor_row.total_runs_game
        
        self.over_under_line_open = visitor_row.over_under_line_open
        self.over_under_line_close = visitor_row.over_under_line_close
        self.over_odds_open = visitor_row.over_under_odds_open
        self.over_odds_close = visitor_row.over_under_odds_close
        self.under_odds_open = home_row.over_under_odds_open
        self.under_odds_close = home_row.over_under_odds_close
        
        self.visitor_team = visitor_row.team
        self.visitor_run_total = visitor_row.team_run_total
        self.visitor_money_line_open = visitor_row.money_line_open
        self.visitor_money_line_close = visitor_row.money_line_close
        self.visitor_pitcher = visitor_row.pitcher
        self.visitor_run_dif = visitor_row.run_dif_game
        self.visitor_run_line_close = visitor_row.run_line_close
        self.visitor_run_line_odds_close = visitor_row.run_line_odds_close
        
        self.home_team = home_row.team
        self.home_run_total = home_row.team_run_total
        self.home_money_line_open = home_row.money_line_open
        self.home_money_line_close = home_row.money_line_close
        self.home_pitcher = home_row.pitcher
        self.home_run_dif = home_row.run_dif_game
        self.home_run_line_close = home_row.run_line_close
        self.home_run_line_odds_close = home_row.run_line_odds_close

    def money_line_bet(self, strategy_func):
        choice = strategy_func(self)
        if choice is None:
            return 0
        elif choice == self.winner():
            return 1
        else:
            return -1

    def winner(self):
        if self.home_run_dif > 0:
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
    games = []
    # for visitor_row, home_row in game_sequence():
    #     games.append(Game(visitor_row, home_row))
    
        # print(g.money_line_bet(home_team))
        # print(g.home_team)
        # print(g.visitor_team)

        
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