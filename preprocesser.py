#! /usr/bin/python3

import numpy as np
import pandas as pd
import functions as f

data=pd.read_csv('finaldata11.csv')
data.pop('Unnamed: 0')
data=data.astype('object')
#data=data[:1000]

c2_avg=['PTS', 'FGM', 'FGA','FG%', '3PM', '3PA', '3P%',
        'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB',
        'AST', 'TOV', 'STL', 'BLK', 'PF', '+/-']

for ix in range(len(data)):
  print(ix)
  data1=data.loc[ix,'Game Date']
  team=data.loc[ix,'Team']
  past=f.get_past_games(data,data1,team,50)
  data.at[ix,'winrate 50']=f.create_winrate(past,50)
  data.at[ix,'winrate 7']=f.create_winrate(past,7)
  
  for c in c2_avg:
    data.at[ix,c]=f.get_avgs(past,c)

data.to_csv('test_corr.csv',index=False)

a=data.loc[[0]]
ix=0
while ix < len(data):
  if ix != 0:
    a=a.append(data.loc[[ix]])
  ix+=2

b=data.loc[[1]]
ix=1
while ix < len(data):
  if ix != 1:
    b=b.append(data.loc[[ix]])
  ix+=2

a=a.reset_index(drop=True)
b=b.reset_index(drop=True)

b=b.join(a,lsuffix='_left',rsuffix='_right')

b['Result']=f.result(b)
b['Location']=f.location(b)

b.to_csv('train.csv',index=False)

