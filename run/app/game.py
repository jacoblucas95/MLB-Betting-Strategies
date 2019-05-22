import os, csv, sqlite3, json
from datetime import date
import numpy as np
import pandas as pd

from app import get_game_data, game_sequence, df, fix_df_types
from strategies import home_team, visitor_team, favorites, underdogs, overs, unders
from game_filter import date_range

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

        if visitor_row.money_line_close < home_row.money_line_close:
            self.visitor_team_is_money_line_favorite = True
            self.favorite_money_line_team = visitor_row.team
            self.favorite_money_line_open = visitor_row.money_line_open
            self.favorite_money_line_close = visitor_row.money_line_close
            self.favorite_money_line_run_dif_game = visitor_row.run_dif_game

            self.underdog_money_line_team = home_row.team
            self.underdog_money_line_open = home_row.money_line_open
            self.underdog_money_line_close = home_row.money_line_close
            self.underdog_money_line_run_dif_game = home_row.run_dif_game
            
        else:
            self.visitor_team_is_money_line_favorite = False
            self.favorite_money_line_team = home_row.team
            self.favorite_money_line_open = home_row.money_line_open
            self.favorite_money_line_close = home_row.money_line_close
            self.favorite_money_line_run_dif_game = home_row.run_dif_game 

            self.underdog_money_line_team = visitor_row.team
            self.underdog_money_line_open = visitor_row.money_line_open
            self.underdog_money_line_close = visitor_row.money_line_close
            self.underdog_money_line_run_dif_game = visitor_row.run_dif_game
        
        if visitor_row.run_line_odds_close < home_row.run_line_odds_close:
            self.visitor_team_is_run_line_favorite = True
            self.favorite_run_line_team = visitor_row.team
            self.favorite_run_line_odds_close = visitor_row.run_line_odds_close
            self.underdog_run_line_odds_close = home_row.run_line_odds_close
            self.underdog_run_line_team = home_row.team
            self.favorite_run_line_run_dif_game = visitor_row.run_dif_game
            self.underdog_run_line_run_dif_game = home_row.run_dif_game

        else:
            self.visitor_team_is_run_line_favorite = False
            self.favorite_run_line_team = home_row.team
            self.favorite_run_line_odds_close = home_row.run_line_odds_close
            self.underdog_run_line_odds_close = visitor_row.run_line_odds_close
            self.underdog_run_line_team = visitor_row.team
            self.underdog_run_line_run_dif_game = visitor_row.run_dif_game
            self.favorite_run_line_run_dif_game = home_row.run_dif_game

    #TODO complete function with odds included

    def run_line_bet(self, strategy_func):
        choice = strategy_func(self)
        if choice is None:
            return 0
        elif self.run_line_winner(choice)[2]:
            return 1 * odds_payout(self.run_line_winner(choice)[0], favorite=self.run_line_winner(choice)[1], win=self.run_line_winner(choice)[2])
        else:
            return -1 * odds_payout(self.run_line_winner(choice)[0], favorite=self.run_line_winner(choice)[1], win=self.run_line_winner(choice)[2])
    
    def run_line_winner(self, choice):
        # returns a tuple (odds, bet_on_favorite=True/False, win_or_lose=True/False)
        if choice == 'h':
            if self.visitor_team_is_run_line_favorite:
                if self.underdog_run_line_run_dif_game > -1.5:
                    return self.underdog_run_line_odds_close, False, True
                else:
                    return self.underdog_run_line_odds_close, False, False
            else:
                if self.favorite_run_line_run_dif_game > 1.5:
                    return self.favorite_run_line_odds_close, True, True
                else:
                    return self.favorite_run_line_odds_close, True, False
        elif choice == 'v':
            if self.visitor_team_is_run_line_favorite:
                if self.favorite_run_line_run_dif_game > 1.5:
                    return self.favorite_run_line_odds_close, True, True
                else:
                    return self.favorite_run_line_odds_close, True, False
            else:
                if self.underdog_run_line_run_dif_game > -1.5:
                    return self.underdog_run_line_odds_close, False, True
                else:
                    return self.underdog_run_line_odds_close, False, False
        elif choice == 'fav':
            if self.favorite_run_line_run_dif_game > 1.5:
                return self.favorite_run_line_odds_close, True, True
            else:
                return self.favorite_run_line_odds_close, True, False
        elif choice == 'dog':
            if self.underdog_run_line_run_dif_game > -1.5:
                return self.underdog_run_line_odds_close, False, True
            else:
                return self.underdog_run_line_odds_close, False, False
        else:
            return ValueError

    def over_under_bet(self, strategy_func):
        choice = strategy_func(self)
        if choice is None:
            return 0
        elif self.over_under_winner(choice) == True:
            return 1
        elif self.over_under_winner(choice) == False:
            return -1
        elif self.over_under_winner(choice) == None:
            return 0
        else:
            return ValueError
    
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

    # def money_line_winner(self, choice):
    #     if choice == 'h':
    #         if self.home_run_dif > 0:
    #             return True
    #         else:
    #             return False
    #     elif choice == 'v':
    #         if self.visitor_run_dif > 0:
    #             return True
    #         else:
    #             return False
    #     elif choice == 'fav':
    #         if self.favorite_run_dif_game > 0:
    #             return True
    #         else:
    #             return False
    #     elif choice == 'dog':
    #         pass
    #     #TODO
    #     else:
    #         ValueError

def odds_payout(odds, favorite, win):
    if win == False:
        return 1
    elif win == True:
        if favorite:
            return 1 / (abs(odds)/100)
        else:
            return abs(odds)/100
    else:
        return 'inputs must be true or false'

def create_betting_results(bet_type, strategy_func, df=df):
    count = 0
    data = []
    for visitor_row, home_row in game_sequence(df):
        game = Game(visitor_row, home_row)
        date = game.date
        gameno = game.gameno
        if bet_type == 'ml':
            bet_outcome = game.money_line_bet(strategy_func)
        elif bet_type == 'ou':
            bet_outcome = game.over_under_bet(strategy_func)
        elif bet_type == 'rl':
            bet_outcome = game.run_line_bet(strategy_func)
        else:
            return None
        count += bet_outcome
        data.append({'Date': date, 'Bet_Outcomes': bet_outcome, 'Portfolio Value': count, 'Gameno':gameno})
    return data
    
if __name__ == "__main__":
    csvData = pd.DataFrame(create_betting_results('rl', underdogs, date_range()))
    csvData.to_csv('test.csv')
