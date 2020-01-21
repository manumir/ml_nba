import numpy as np
import pandas as pd
import functions as f
import time

start_time = time.time()

data=pd.read_csv('whole_raw.csv')
data=data.dropna()
og_data=data
data=data.astype('object')

c2_avg=['PTS', 'FGM', 'FGA','FG%', '3PM', '3PA', '3P%',
        'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB',
        'AST', 'TOV', 'STL', 'BLK', 'PF', '+/-']

for ix in range(len(data)):
  print(ix)
  data1=data.loc[ix,'Game Date']
  team=data.loc[ix,'Team']
  past=f.get_past_games(og_data,data1,team,20)
  data.at[ix,'winrate 20']=f.create_winrate(past,20)
  data.at[ix,'winrate 10']=f.create_winrate(past,10)
  data.at[ix,'winrate 5']=f.create_winrate(past,5)
  data.at[ix,'fatigue']=f.fatigue(past)

  for c in c2_avg:
    data.at[ix,c]=f.get_avgs(past,c)

#data.to_csv('data.csv',index=False)

b=f.append2for1(data)
b['Result']=f.result(b)

b.to_csv('train.csv',index=False)

print("run in %s seconds" % (time.time() - start_time))
