import pandas as pd
import functions as f
from sklearn import svm
from sklearn.preprocessing import scale
from sklearn.model_selection import train_test_split
import os

curr_path=os.getcwd()
path2data=curr_path[:-6]

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
 
clf = svm.LinearSVC(random_state=2)

# split data into train and test sets
Y=data.pop('Result')
X=data
x_train,x_test,y_train,y_test = train_test_split(X, Y, test_size=0.2, random_state=1)
x_train,x_test=scale(x_train),scale(x_test)
clf.fit(x_train,y_train)
preds=clf.predict(x_test)
print('zeros:',f.get0and1(preds))
print('test:',f.acc(preds,y_test))
#joblib.dump(clf,'regression_linear.joblib')

# predict today's games
games=pd.read_csv(path2data+'games.csv')
data=pd.read_csv(path2data+'data.csv')
for game in list(range(len(games))):
	home=data.loc[data['Team']==games.at[game,'home']]
	away=data.loc[data['Team']==games.at[game,'away']]
	home=home.reset_index(drop=True)
	away=away.reset_index(drop=True)
	home=home.loc[[game]]
	away=away.loc[[game]]
	
	print('home: ',home['Team'].values,'away: ',away['Team'].values)

	home=home[['PTS','FGM','FGA','FG%','3PM','3PA','3P%','FTM','FTA','FT%',
	'OREB','DREB','REB','AST','TOV','STL','BLK','PF','+/-','winrate 20','winrate 10','winrate 5']]
	away=away[['PTS','FGM','FGA','FG%','3PM','3PA','3P%','FTM','FTA','FT%',
	'OREB','DREB','REB','AST','TOV','STL','BLK','PF','+/-','winrate 20','winrate 10','winrate 5']]
	
	b=home.join(away,lsuffix='_home',rsuffix='_away')
	b=b.drop(del2,1)
	print(clf.predict(b))
