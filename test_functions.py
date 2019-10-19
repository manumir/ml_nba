import pandas as pd

import functions as f

a=pd.read_csv('whole_data_raw.csv')

games=f.get_past_games(a,'11/30/2001','SEA',3)
df=a.loc[games]

avgs=f.get_avgs(df,'PTS')

print(df,avgs)
