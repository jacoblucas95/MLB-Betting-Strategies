import os, csv, sqlite3, json
from os.path import dirname
from datetime import date
import pprint
import numpy as np
import pandas as pd

from app import get_game_data, game_sequence, fix_df_types
from strategies import home_team, visitor_team, favorites, underdogs, overs, unders
from game_filter import date_range
from app import df

class Game:
    def __init__(self, visitor_row, home_row):
        self.date = visitor_row.date.date()
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

        if visitor_row.money_line_close < 0:
            self.fav_ml = visitor_row.money_line_close
            self.fav_run_dif = visitor_row.run_dif_game
        else:
            self.fav_ml = home_row.money_line_close
            self.fav_run_dif = home_row.run_dif_game

    #TODO complete function with odds included

    def run_line_bet(self, strategy_func):
        choice = strategy_func(self)
        if choice is None:
            return 0
        elif self.run_line_winner(choice):
            return 1
        else:
            return -1
    
    def run_line_winner(self, choice):
        if choice == 'H':
            if self.home_run_line_odds_close < 0:
                if self.home_run_dif > 1.5:
                    return True
                else:
                    return False
            else:
                if self.visitor_run_dif > 1.5:
                    return False
                else:
                    return True
        elif choice == 'V':
            if self.visitor_run_line_odds_close < 0:
                if self.visitor_run_dif > 1.5:
                    return True
                else:
                    return False
            else:
                if self.home_run_dif > 1.5:
                    return False
                else:
                    return True
        else:
            return ValueError

    def over_under_bet(self, strategy_func):
        choice = strategy_func(self)
        if choice is None:
            return 0
        elif self.over_under_winner(choice):
            return 1
        else:
            return -1
    
    def over_under_winner(self, choice):
        if choice == 'o':
            if self.total_runs_game > self.over_under_line_close:
                return True
            elif self.total_runs_game < self.over_under_line_close:
                return False
            else:
                return None
        elif choice == 'u':
            if self.total_runs_game > self.over_under_line_close:
                return False
            elif self.total_runs_game < self.over_under_line_close:
                return True
            else:
                return None
        else:
            return ValueError
    
    def money_line_bet(self, strategy_func):
        choice = strategy_func(self)
        if choice is None:
            return 0
        elif self.money_line_winner(choice):
            return 1
        else:
            return -1

    def money_line_winner(self, choice):
        if choice == 'H':
            if self.home_run_dif > 0:
                return True
            else:
                return False
        elif choice == 'V':
            if self.visitor_run_dif > 0:
                return True
            else:
                return False
        else:
            ValueError

def odds_payout(odds):
    if odds > 0:
        return abs(odds)/100
    else:
        return 1 / (abs(odds)/100)

def create_betting_results(bet_type, strategy_func, df=df):
    count = 0
    data = []
    for visitor_row, home_row in game_sequence(df):
        game = Game(visitor_row, home_row)
        date = game.date
        if bet_type == 'ml':
            bet_outcome = game.money_line_bet(strategy_func)
        elif bet_type == 'ou':
            bet_outcome = game.over_under_bet(strategy_func)
        elif bet_type == 'rl':
            bet_outcome = game.run_line_bet(strategy_func)
        else:
            return None
        count += bet_outcome
        data.append({'Date': date, 'Bet_Outcomes': bet_outcome, 'Portfolio Value': count})
    return data
    
if __name__ == "__main__":
    print(create_betting_results('ou', overs, date_range()))
    
    # write_to_testcsv()
    # pd.DataFrame(data).to csv('test.csv', index=False)
    # for visitor_row, home_row in game_sequence(df=date_range()):
    #     games.append(Game(visitor_row, home_row))
    #     return games
