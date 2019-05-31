import os, csv, sqlite3, json
from datetime import datetime
import numpy as np
import pandas as pd

from .handler import get_game_data, game_sequence
from .strategies import home, visitor, overs, underdogs, unders, favorites, home_underdogs_ml, visitor_favorites_ml, visitor_underdogs_ml, visitor_underdogs_rl, home_favorites_ml, home_favorites_rl
from .game_filter import Filter


class Game:
    def __init__(self, game_row):
        self.date = game_row.date
        self.gameno = game_row.gameno
        self.total_runs_game = game_row.total_runs_game
        
        self.over_line_open = game_row.over_line_open
        self.over_line_close = game_row.over_line_close
        self.over_odds_open = game_row.over_odds_open
        self.over_odds_close = game_row.over_odds_close
        self.under_odds_open = game_row.under_odds_open
        self.under_odds_close = game_row.under_odds_close
        
        self.v_team = game_row.v_team
        self.v_team_run_total = game_row.v_team_run_total
        self.v_money_line_open = game_row.v_money_line_open
        self.v_money_line_close = game_row.v_money_line_close
        self.v_pitcher = game_row.v_pitcher
        self.v_run_dif_game = game_row.v_run_dif_game
        self.v_run_line_close = game_row.v_run_line_close
        self.v_run_line_odds_close = game_row.v_run_line_odds_close

        self.h_team = game_row.h_team
        self.h_team_run_total = game_row.h_team_run_total
        self.h_money_line_open = game_row.h_money_line_open
        self.h_money_line_close = game_row.h_money_line_close
        self.h_pitcher = game_row.h_pitcher
        self.h_run_dif_game = game_row.h_run_dif_game
        self.h_run_line_close = game_row.h_run_line_close
        self.h_run_line_odds_close = game_row.h_run_line_odds_close
        
        if game_row.over_odds_close < game_row.under_odds_close:
            self.over_is_favorite = True
        else:
            self.over_is_favorite = False
        
        if self.v_money_line_close < self.v_money_line_open:
            self.visitor_team_is_money_line_public_favorite = True
        else:
            self.visitor_team_is_money_line_public_favorite = False
        
        if self.h_money_line_close < self.h_money_line_open:
            self.home_team_is_money_line_public_favorite = True
        else:
            self.home_team_is_money_line_public_favorite = False

        if game_row.v_money_line_close < game_row.h_money_line_close:
            self.visitor_team_is_money_line_favorite = True
            self.favorite_money_line_team = game_row.v_team
            self.favorite_money_line_open = game_row.v_money_line_open
            self.favorite_money_line_close = game_row.v_money_line_close
            self.favorite_money_line_run_dif_game = game_row.v_run_dif_game

            self.underdog_money_line_team = game_row.h_team
            self.underdog_money_line_open = game_row.h_money_line_open
            self.underdog_money_line_close = game_row.h_money_line_close
            self.underdog_money_line_run_dif_game = game_row.h_run_dif_game
            
        else:
            self.visitor_team_is_money_line_favorite = False
            self.favorite_money_line_team = game_row.h_team
            self.favorite_money_line_open = game_row.h_money_line_open
            self.favorite_money_line_close = game_row.h_money_line_close
            self.favorite_money_line_run_dif_game = game_row.h_run_dif_game 

            self.underdog_money_line_team = game_row.v_team
            self.underdog_money_line_open = game_row.v_money_line_open
            self.underdog_money_line_close = game_row.v_money_line_close
            self.underdog_money_line_run_dif_game = game_row.v_run_dif_game
        
        if game_row.v_run_line_close < game_row.h_run_line_close:
            self.visitor_team_is_run_line_favorite = True
            self.favorite_run_line_team = game_row.v_team
            self.favorite_run_line_odds_close = game_row.v_run_line_odds_close
            self.underdog_run_line_odds_close = game_row.h_run_line_odds_close
            self.underdog_run_line_team = game_row.h_team
            self.favorite_run_line_run_dif_game = game_row.v_run_dif_game
            self.underdog_run_line_run_dif_game = game_row.h_run_dif_game

        else:
            self.visitor_team_is_run_line_favorite = False
            self.favorite_run_line_team = game_row.h_team
            self.favorite_run_line_odds_close = game_row.h_run_line_odds_close
            self.underdog_run_line_odds_close = game_row.v_run_line_odds_close
            self.underdog_run_line_team = game_row.v_team
            self.underdog_run_line_run_dif_game = game_row.v_run_dif_game
            self.favorite_run_line_run_dif_game = game_row.h_run_dif_game

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
        elif self.over_under_winner(choice) == None:
            return 0
        elif self.over_under_winner(choice)[2]:
            return 1 * odds_payout(self.over_under_winner(choice)[0], favorite=self.over_under_winner(choice)[1], win=self.over_under_winner(choice)[2])
        elif self.over_under_winner(choice)[2] == False:
            return -1 * odds_payout(self.over_under_winner(choice)[0], favorite=self.over_under_winner(choice)[1], win=self.over_under_winner(choice)[2])
        else:
            return ValueError

    def over_under_winner(self, choice):
        def convert_choice(choice):
            if choice == 'fav':
                if self.over_is_favorite:
                    return 'o'
                else:
                    return 'u'
            else:
                if self.over_is_favorite:
                    return 'u'
                else:
                    return 'o'
        if choice == 'fav' or choice == 'dog':
            choice = convert_choice(choice)
        # returns a tuple (odds, bet_on_favorite=True/False, win_or_lose=True/False)
        if self.total_runs_game == self.over_line_close:
            return None
        if choice == 'o':
            if self.over_is_favorite:
                if self.total_runs_game > self.over_line_close:
                    return self.over_odds_close, True, True
                else:
                    return self.over_odds_close, True, False
            else:
                if self.total_runs_game > self.over_line_close:
                    return self.over_odds_close, False, True
                else:
                    return self.over_odds_close, False, False
        elif choice == 'u':
            if self.over_is_favorite:
                if self.total_runs_game > self.over_line_close:
                    return self.under_odds_close, False, False
                else:
                    return self.under_odds_close, False, True
            else:    
                if self.total_runs_game > self.over_line_close:
                    return self.under_odds_close, True, False
                else:
                    return self.under_odds_close, True, True
        else:
            return ValueError
    
    def money_line_bet(self, strategy_func):
        choice = strategy_func(self)
        if choice is None:
            return 0
        elif self.money_line_winner(choice)[2]:
            return 1 * odds_payout(self.money_line_winner(choice)[0], favorite=self.money_line_winner(choice)[1], win=self.money_line_winner(choice)[2])
        else:
            return -1 * odds_payout(self.money_line_winner(choice)[0], favorite=self.money_line_winner(choice)[1], win=self.money_line_winner(choice)[2])

    def money_line_winner(self, choice):
            # returns a tuple (odds, bet_on_favorite=True/False, win_or_lose=True/False)
            if choice == 'h':
                if self.visitor_team_is_money_line_favorite:
                    if self.underdog_money_line_run_dif_game > 0:
                        return self.underdog_money_line_close, False, True
                    else:
                        return self.underdog_money_line_close, False, False
                else:
                    if self.favorite_money_line_run_dif_game > 0:
                        return self.favorite_money_line_close, True, True
                    else:
                        return self.favorite_money_line_close, True, False
            elif choice == 'v':
                if self.visitor_team_is_money_line_favorite:
                    if self.favorite_money_line_run_dif_game > 0:
                        return self.favorite_money_line_close, True, True
                    else:
                        return self.favorite_money_line_close, True, False
                else:
                    if self.underdog_money_line_run_dif_game > 0:
                        return self.underdog_money_line_close, False, True
                    else:
                        return self.underdog_money_line_close, False, False
            elif choice == 'fav':
                if self.favorite_money_line_run_dif_game > 0:
                    return self.favorite_money_line_close, True, True
                else:
                    return self.favorite_money_line_close, True, False
            elif choice == 'dog':
                if self.underdog_money_line_run_dif_game > 0:
                    return self.underdog_money_line_close, False, True
                else:
                    return self.underdog_money_line_close, False, False
            else:
                return ValueError

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

#TODO Make this function faster
def create_betting_results(bet_type, strategy_func, bet_amt, df):
    count = 0
    data = []
    for game_row in game_sequence(df):
        game = Game(game_row)
        date_ = game.date
        gameno = game.gameno
        if bet_type == 'ml':
            bet_outcome = game.money_line_bet(strategy_func)
        elif bet_type == 'ou':
            bet_outcome = game.over_under_bet(strategy_func)
        elif bet_type == 'rl':
            bet_outcome = game.run_line_bet(strategy_func)
        else:
            return None
        count += (bet_amt * bet_outcome)
        data.append({'date': int(date_), 'bet_outcomes': float(bet_outcome), 'portfolio_value': float(count), 'gameno': int(gameno)})
    df2 = pd.DataFrame.from_dict(data)
    df2.drop(['date'], axis=1, inplace=True)
    df3 = pd.merge(df, df2, on='gameno', how='right')
    pickle_path = os.path.join(os.path.dirname(__file__), '..', 'setup', 'data', 'analysis_dataset.pickle')
    df3.to_pickle(pickle_path)
    return data

def create_betting_results_test(bet_type, strategy_func, bet_amt, df):
    count = 0
    data = []
    for game_row in game_sequence(df):
        game = Game(game_row)
        date_ = game.date
        gameno = game.gameno
        if bet_type == 'ml':
            bet_outcome = game.money_line_bet(strategy_func)
        elif bet_type == 'ou':
            bet_outcome = game.over_under_bet(strategy_func)
        elif bet_type == 'rl':
            bet_outcome = game.run_line_bet(strategy_func)
        else:
            return None
        count += (bet_amt * bet_outcome)
        data.append({'date': str(date_), 'bet_outcomes': float(bet_outcome), 'portfolio_value': float(count), 'gameno': int(gameno)})
    df2 = pd.DataFrame.from_dict(data)
    df3 = pd.merge(df, df2, on='gameno', how='right')
    pickle_path = os.path.join(os.path.dirname(__file__), '..', 'setup', 'data', 'analysis_dataset.pickle')
    df3.to_pickle(pickle_path)
    return data
    
'''
if __name__ == "__main__":
    pass
#    print(create_betting_results('ml', favorites, 100))
#    csvData.to_csv('test.csv')
'''