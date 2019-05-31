import os, sys
import numpy as np
import pandas as pd

def summary_stats(df):
    summary = []
    win_count = 0
    win_index_ls = []
    loss_count = 0
    push_count = 0
    for index, row in df.iterrows():
        w_l = row['bet_outcomes']
        if w_l > 0:
            win_count += 1
            win_index_ls.append(index)
        elif w_l < 0:
            loss_count += 1
        else:
            push_count += 1

    win_df = df.iloc[win_index_ls, :]

    w_avg = win_df['bet_outcomes'].mean()
    w_std = win_df['bet_outcomes'].std()

    summary.append({'wins': win_count, 'losses': loss_count, 'pushes': push_count, 'win_amount_avg': w_avg, 'win_amount_std': w_std})
    return summary