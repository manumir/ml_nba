import numpy as np

# create a data frame of games before a certain date
def get_past_games(df,data1,team,amount):
  rows=df.loc[df['Team'] == team]
  rows=rows.loc[rows['Game Date'] < data1]
  return rows[-(amount):]

#averages for each column 
def get_avgs(df,column):
  count=0
  try:
    for x in df[column].values:
      count+=int(x)
    avg=float(count/len(df[column].values))
    return avg
  except Exception as e:
    return np.nan

def create_winrate(df,amount):
  try:
    df=df[-(amount):]
    b=0
    for x in df['W/L'].values:
      if x == 'W':
        b+=1
    return float(b/amount)
  except:
    return np.nan

def result(df):
    results=[]
    for value in df['W/L_right'].values:
        if value=='L':
            results.append(0)
        else:
            results.append(1)
    return results

def location(df):
    locations=[]
    for value in df['Match Up_right'].values:
        if value[4]=='v':
            locations.append(0)
        else:
            locations.append(1)
    return locations

def append2for1(data):
  a=data.loc[[0]]
  ix=0
  while ix < len(data):
    print(ix)
    if ix != 0:
      a=a.append(data.loc[[ix]])
    ix+=2

  b=data.loc[[1]]
  ix=1
  while ix < len(data):
    print(ix)
    if ix != 1:
      b=b.append(data.loc[[ix]])
    ix+=2

  a=a.reset_index(drop=True)
  b=b.reset_index(drop=True)
  b=b.join(a,lsuffix='_left',rsuffix='_right')
  
  return b

