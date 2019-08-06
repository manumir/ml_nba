import pandas as pd

import functions as f

a=pd.read_csv('finaldata11.csv')
a.pop('Unnamed: 0')

games=f.get_past_games(a,'04/23/2012','GSW',3)
df=a.loc[games]

avgs=f.get_avgs(df,'PTS')

print(df,avgs)
