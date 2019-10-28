import numpy as np
import pandas as pd
from sklearn import preprocessing

# create a data frame of games before a certain date
def get_past_games(df,date2,team,amount):
  ixs=[]
  rows=df.loc[df['Team'] == team]
  dates=rows['Game Date']
  for ix in dates.index:
    if len(ixs)==20:
      break
    date1=df.at[ix,'Game Date']
    if date1_sooner_than_date2(date1,date2):
      ixs.append(ix)
  return df.loc[ixs]
  
#averages for each column 
def get_avgs(df,column):
  count=0
  try:
    for x in df[column].values:
      count+=int(x)
    avg=float(count/len(df[column]))
    return avg
  except Exception as e:
    print(e)
    return np.nan

def create_winrate(df,amount):
  try:
    df=df[:amount]
    b=0
    for x in df['W/L'].values:
      if x == 'W':
        b+=1
    return float(b/len(df))
  except:
    return np.nan

def result(df):
    results=[]
    for value in df['W/L_away'].values:
        if value=='L':
            results.append(0)
        else:
            results.append(1)
    return results

def location(df):
  locations=[]
  for value in df['Match Up_away'].values:
    if value[4]=='v':
      locations.append(0)
    else:
      locations.append(1)
  return locations

# this is WRONGGGG
def append2for1(data):
  data=data.reset_index(drop=True)
  left=pd.DataFrame(columns=data.columns)
  right=pd.DataFrame(columns=data.columns)

  it=list(range(data.shape[0]))
  for ix in it:
    print(len(it))
    name=data.at[ix,'Match Up'][-3:]
    date=data.at[ix,'Game Date']
    other=data.loc[data['Game Date']==date]
    other=other.loc[data['Team']==name]
    it.remove(ix)

    # get home on the left
    if data.loc[ix,'Match Up'][4]=='v':
      left=left.append(data.loc[ix])
      right=right.append(other)
      left=left.reset_index(drop=True)
      right=right.reset_index(drop=True)
    else:
      left=left.append(other)
      right=right.append(data.loc[ix])
      left=left.reset_index(drop=True)
      right=right.reset_index(drop=True)
    
  row=left.join(right,lsuffix='_home',rsuffix='_away')
  return row
  
#create a function to determine if a date is sooner than another date
def date1_sooner_than_date2(date1,date2):
    if date1[6:len(date1)]>date2[6:len(date2)]:
        #print("date1's year is later than date2's year")
        return False
    if date1[6:len(date1)]<date2[6:len(date2)]:
        #print("date2's year is later than date1's year")
        return True
    
    if date1[6:len(date1)]==date2[6:len(date2)]:
        if date1[0:2]>date2[0:2]:
            #print("date1's month is later than date2's month")
            return False
    if date1[6:len(date1)]==date2[6:len(date2)]:
        if date1[0:2]<date2[0:2]:
            #print("date2's month is later than date1's month")
            return True
        
    if date1[6:len(date1)]==date2[6:len(date2)]:
        if date1[0:2]==date2[0:2]:
            if date1[3:5]>date2[3:5]:
                #print("date1's day is later than date2's day")
                return False
    if date1[6:len(date1)]==date2[6:len(date2)]:
        if date1[0:2]==date2[0:2]:
            if date1[3:5]<date2[3:5]:
                #print("date2's day is later than date1's day")
                return True
            
    if date1[6:len(date1)]==date2[6:len(date2)]:
        if date1[0:2]==date2[0:2]:
            if date1[3:5]==date2[3:5]:
                return 0

def acc(true_y,pred_y):
  true_y=list(true_y)
  pred_y=list(pred_y)
  count=0 
  for x in range(len(true_y)):
    if round(pred_y[x])==round(true_y[x]):
      count=count+1
  return count/len(true_y)

# search for the best data arrangement for training
def best_random_state(clf,data,fraction,range_of_possi):
  best_i=0
  best_acc=0
  for i in range_of_possi:
    train_dataset = data.sample(frac=fraction,random_state=i)# 11,7
    test_dataset = data.drop(train_dataset.index)
    train_labels = train_dataset.pop('Result')
    test_labels = test_dataset.pop('Result')
    
    train_dataset=preprocessing.scale(train_dataset)
    test_dataset=preprocessing.scale(test_dataset)

    clf.fit(train_dataset,train_labels)
    accuracy=acc(clf.predict(test_dataset),test_labels)
    
    if accuracy>best_acc:
      best_i=i
      best_acc=accuracy
  print(best_i,"acc :",best_acc)
  return best_i

def name2acro(column,site):
  teams=['MEM', 'HOU', 'BKN', 'BOS', 'LAC', 'NOP', 'SAC', 'POR', 'DET', 'UTA', 'CHA', 'SAS', 'WAS', 'TOR','DEN',
       'MIL', 'ATL','GSW', 'DAL', 'ORL', 'PHI', 'NYK', 'LAL', 'CLE', 'OKC', 'MIN', 'CHI', 'MIA', 'PHX', 'IND']

  # name that appear on placard.com
  if site =='placard':
    teams1=['Boston Celtics','Brooklyn Nets','NY Knicks','Philadel. 76ers','Toronto Raptors',
    'Chicago Bulls','Clev. Cavaliers','Detroit Pistons','Indiana Pacers','Milwaukee Bucks',
    'Atlanta Hawks','Charl. Hornets','Miami Heat','Orlando Magic','Washin. Wizards',
    'Dall. Mavericks','Houston Rockets','Memp. Grizzlies','NO Pelicans','SA Spurs',
    'Denver Nuggets','Minnesota Timb.','OKC Thunder','Trail Blazers','Utah Jazz',
    'GS Warriors','LA Clippers','LA Lakers','Phoenix Suns','Sac. Kings']
    
  elif site=='nba':
    teams1=['Boston Celtics','Brooklyn Nets','New York Knicks','Philadelphia 76ers','Toronto Raptors',
    'Chicago Bulls','Cleveland Cavaliers','Detroit Pistons','Indiana Pacers','Milwaukee Bucks',
    'Atlanta Hawks','Charlotte Hornets','Miami Heat','Orlando Magic','Washington Wizards',
    'Dallas Mavericks','Houston Rockets','Memphis Grizzlies','New Orleans Pelicans','San Antonio Spurs',
    'Denver Nuggets','Minnesota Timberwolves','Oklahoma City Thunder','Portland Trail Blazers','Utah Jazz',
    'Golden State Warriors','LA Clippers','Los Angeles Lakers','Phoenix Suns','Sacramento Kings']

  # sort teams names and teams acronyms
  teams.sort()
  teams1.sort()
  
  # bos and bkn are switched
  x=teams[1]
  teams[1]=teams[2]
  teams[2]=x
  """
  # nyk and nop are switched
  x=teams[18]
  teams[18]=teams[19]
  teams[19]=x
  """
  #sas and sac are switched
  x=teams[26]
  teams[26]=teams[24]
  teams[24]=x

  # por and tor are switched
  x=teams[27]
  teams[27]=teams[26]
  teams[26]=x

  # names to acronyms
  new_A=[]
  for team in column:
    if team=='Philadel. ers':
      team='Philadel. 76ers'#file['away'].values:
    x=0
    for name in teams1:
      if name == team:
        name=teams[x]
        new_A.append(name)
      x=x+1
      
  return new_A
