import pandas as pd
import numpy as np
import os

pickle_path = os.path.join(os.path.dirname(__file__), '..', '..', 'portfolio_testing', 'portfolio_test.pickle')
df = pd.read_pickle(pickle_path)

def performance():
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    outcomes = df.filter(like="outcome", axis=1)
    outcomes.fillna(0)
    avg = outcomes.mean(axis=0)
    average_dict = {}
    for k,v in avg.iteritems():
        average_dict[k] = v
    return average_dict
