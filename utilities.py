import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from collections import Counter
import matplotlib.ticker as ticker
from adjustText import adjust_text

# Filter and suppress only the specific warning related to data validation
warnings.filterwarnings("ignore")

def read_data(filepath: str = 'data/Punteggi.xlsx') -> list[str]:
    players = pd.read_excel(filepath, sheet_name=1, header=None)
    players = players.rename(columns={0: 'player', 1: 'score'})
    return players['player'].tolist()
