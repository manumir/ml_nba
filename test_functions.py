import pandas as pd

import functions as f

a=pd.read_csv('finaldata11.csv')
a.pop('Unnamed: 0')

games=f.get_past_games(a,'04/23/2006','GSW',3)

avgs=f.get_avgs(games,'PTS')

print(avgs)
