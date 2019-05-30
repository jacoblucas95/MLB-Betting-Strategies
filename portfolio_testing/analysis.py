import os
from datetime import datetime, date
from functools import reduce
from pprint import pprint
import numpy as np
import pandas as pd

# from .run import app
from game import Game, create_betting_results, create_betting_results_for_port, df, test_df
from strategies import home, visitor, overs, underdogs, unders, favorites, home_underdogs_ml, visitor_favorites_ml, visitor_underdogs_ml, home_favorites_ml, home_favorites_rl, visitor_underdogs_rl, home_underdogs_rl, visitor_favorites_rl, longshot_teams_rl, longshot_teams_ml

port_pickle_path = os.path.join(os.path.dirname(__file__), 'portfolio.pickle')

def create_portfolio_df(df=df):
    strategy_dict = {'ml': [home, visitor, favorites, underdogs, home_underdogs_ml, visitor_favorites_ml, visitor_underdogs_ml, home_favorites_ml, longshot_teams_ml], 'rl': [home, visitor, favorites, underdogs, home_favorites_rl, visitor_underdogs_rl, home_underdogs_rl, visitor_favorites_rl, longshot_teams_rl], 'ou': [overs, unders, favorites, underdogs]}
    df_list = []
    for group, strategy in strategy_dict.items():
        for strat in strategy:
            results = create_betting_results_for_port(group, strat, 100, df)
            df_list.append(results)
    port_results = reduce(lambda df1, df2: pd.merge(df1, df2, on='gameno', how='right'), df_list)
    pd.to_pickle(port_results, port_pickle_path)
    return port_results

if __name__ == "__main__":
    create_portfolio_df()
    # print(port())


# JUST FOR REFERENCE
# def create_betting_results_test(bet_type, strategy_func, bet_amt, df=test_df):
#     count = 0
#     data = []
#     for game_row in game_sequence(df):
#         game = Game(game_row)
#         date_ = game.date
#         gameno = game.gameno
#         if bet_type == 'ml':
#             bet_outcome = game.money_line_bet(strategy_func)
#         elif bet_type == 'ou':
#             bet_outcome = game.over_under_bet(strategy_func)
#         elif bet_type == 'rl':
#             bet_outcome = game.run_line_bet(strategy_func)
#         else:
#             return None
#         count += (bet_amt * bet_outcome)
#         data.append({'date': str(date_), 'bet_outcomes': float(bet_outcome), 'portfolio_value': float(count), 'gameno': int(gameno)})
#     df2 = pd.DataFrame.from_dict(data)
#     df3 = pd.merge(df, df2, on='gameno', how='right')
#     return data






