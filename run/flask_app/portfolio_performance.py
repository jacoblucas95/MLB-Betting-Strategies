import pandas as pd
import numpy as np
import os

pickle_path = os.path.join(os.path.dirname(__file__), '..', '..', 'portfolio_testing', 'portfolio_test.pickle')
df = pd.read_pickle(pickle_path)

def performance():
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    outcomes = df.filter(like="outcome", axis=1)
    outcomes.fillna(0)
    outcomes.rename(columns={'home_bet_outcomes_ml':'Home ML', 'visitor_bet_outcomes_ml': 'Visitor ML',
                         'favorites_bet_outcomes_ml': 'Favorite ML', 'underdogs_bet_outcomes_ml': 'Underdog ML',
                         'home_underdogs_ml_bet_outcomes_ml': 'Home Underdog ML', 'home_favorites_ml_bet_outcomes_ml': 'Home Favorite ML',
                         'visitor_favorites_ml_bet_outcomes_ml': 'Visitor Favorite ML', 'visitor_underdogs_ml_bet_outcomes_ml': 'Visitor Underdog ML',
                         'longshot_teams_ml_bet_outcomes_ml': 'Longshot ML', 'home_bet_outcomes_rl': 'Home RL',
                         'visitor_bet_outcomes_rl': 'Visitor RL', 'favorites_bet_outcomes_rl': 'Favorite RL',
                         'underdogs_bet_outcomes_rl': 'Underdog RL', 'home_favorites_rl_bet_outcomes_rl': 'Home Favorite RL',
                         'visitor_underdogs_rl_bet_outcomes_rl': 'Visitor Underdog RL', 'home_underdogs_rl_bet_outcomes_rl': 'Home Underdog RL',
                         'visitor_favorites_rl_bet_outcomes_rl': 'Visitor Favorite RL', 'longshot_teams_rl_bet_outcomes_rl': 'Longshot RL',
                         'overs_bet_outcomes_ou': 'Overs OU', 'unders_bet_outcomes_ou': 'Unders OU',
                         'favorites_bet_outcomes_ou': 'Favorites OU', 'underdogs_bet_outcomes_ou': 'Underdogs OU'
                        }, inplace=True)
    avg = outcomes.mean(axis=0)
    average_dict = {}
    for k,v in avg.iteritems():
        average_dict[k] = v

    data = []

    for k, v in average_dict.items():
        bar_dict = {'strategy': k, 'outcome': v*100}

        data.append(bar_dict)

    return data
