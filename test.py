import pandas as pd
import functions as f

file=pd.read_csv('whole_raw.csv')

print(f.get_past_home_games(file,'02/07/2020','LAL',5))
