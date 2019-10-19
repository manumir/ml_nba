import pandas as pd

import functions as f

a=pd.read_csv('whole_data_raw.csv')
a=pd.read_csv('train.csv')

games=f.get_past_games(a,'11/02/2001','DET',3)
df=a.loc[games]

avgs=f.get_avgs(df,'PTS')

print(df,avgs)
