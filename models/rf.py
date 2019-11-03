import pandas as pd
import functions as f
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
import os

curr_path=os.getcwd()
path2data=curr_path[:-6]

path2logs=curr_path[:-6]+'\\logs\\'
log=pd.read_csv(path2logs+'rf_log.csv')

data=pd.read_csv(path2data+'train.csv')
data=data.dropna()
data=data.drop(['Team_home','Match Up_home','Game Date_home','Team_away',
           'Match Up_away','Game Date_away','MIN_home','MIN_away',
           'W/L_home','W/L_away'],1)

corr=data.corr()['Result']
del2=[]
for x in corr.index:
  if abs(corr[x]) < 0.07:
    del2.append(x)
data=data.drop(del2,1)

clf = RandomForestClassifier(n_estimators=100, random_state=11,n_jobs=-1)
fraction=0.95
train_dataset = data.sample(frac=fraction,random_state=f.best_random_state(clf,data,fraction,list(range(150))))
test_dataset = data.drop(train_dataset.index)
train_labels = train_dataset.pop('Result')
test_labels = test_dataset.pop('Result')
clf.fit(train_dataset,train_labels)
print(f.acc(clf.predict(test_dataset),test_labels))
#joblib.dump(clf,'regression_linear.joblib')

games=pd.read_csv(path2data+'games.csv')
df2log=pd.DataFrame()
df2log['home']=games['home']
df2log['away']=games['away']
df2log['date']=games['date']

# predict today's games
preds=[]
data=pd.read_csv(path2data+'data.csv')
for game in list(range(len(games))):
	home=data.loc[data['Team']==games.at[game,'home']]
	away=data.loc[data['Team']==games.at[game,'away']]
	home=home.reset_index(drop=True)
	away=away.reset_index(drop=True)
	home=home.loc[[game]]
	away=away.loc[[game]]

	home=home[['PTS','FGM','FGA','FG%','3PM','3PA','3P%','FTM','FTA','FT%',
	'OREB','DREB','REB','AST','TOV','STL','BLK','PF','+/-','winrate 20','winrate 10','winrate 5']]
	away=away[['PTS','FGM','FGA','FG%','3PM','3PA','3P%','FTM','FTA','FT%',
	'OREB','DREB','REB','AST','TOV','STL','BLK','PF','+/-','winrate 20','winrate 10','winrate 5']]
	
	b=home.join(away,lsuffix='_home',rsuffix='_away')
	b=b.drop(del2,1)
	preds.append(clf.predict(b))

df2log['rf']=preds
df2log=df2log.sort_values('home')
log=log.append(df2log,sort=False)
log.to_csv(path2logs+'rf_log.csv',index=False)
