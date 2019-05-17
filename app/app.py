import os
import pandas as pd
import numpy as np

csvfile = os.path.join(os.path.dirname(os.getcwd()), 'setup', 'data', 'baseball.csv')
df = pd.read_csv(csvfile, low_memory=False)

if __name__ == "__main__":
    pass
