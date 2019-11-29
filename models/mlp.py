import pandas as pd
import functions as f
from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing
import os

curr_path=os.getcwd()
path2data=curr_path[:-6]

#os.mkdir(curr_path[:-6]+'\\logs\\')
path2logs=curr_path[:-6]+'\\logs\\'
#log=pd.read_csv(path2logs+'mlp_log.csv')

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

clf = MLPClassifier(activation='logistic',random_state=1,max_iter=500)
train_dataset = data.sample(frac=0.99,random_state=12)#f.best_random_state(clf,data,0.9,list(range(20))))
test_dataset = data.drop(train_dataset.index)
train_labels = train_dataset.pop('Result')
test_labels = test_dataset.pop('Result')
clf.fit(train_dataset,train_labels)
preds=clf.predict(test_dataset)
print('zeros: ',f.get0and1(preds))
print('test: ',f.acc(preds,test_labels))
#joblib.dump(clf,'regression_linear.joblib')

games=pd.read_csv(path2data+'games.csv')
df2log=pd.DataFrame()
df2log['home']=games['home']
df2log['away']=games['away']
df2log['date']=games['date']

# predict today's games
c2_avg=['PTS', 'FGM', 'FGA','FG%', '3PM', '3PA', '3P%',
        'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB',
        'AST', 'TOV', 'STL', 'BLK', 'PF', '+/-']

preds=[]
data=pd.read_csv(path2data+'whole_raw.csv')
for game in range(len(games)):
	b=pd.DataFrame()
	team_home=games.at[game,'home']
	team_away=games.at[game,'away']
	teams=[team_home,team_away]
	date=games.at[game,'date']
	
	x,teams_avgs=0,pd.DataFrame()
	for team in teams:
		past=f.get_past_games(data,date,team,20)
		for c in c2_avg:
			b.at[x,c]=f.get_avgs(past,c)
		b.at[x,'winrate 20']=f.create_winrate(past,20)
		b.at[x,'winrate 10']=f.create_winrate(past,10)
		b.at[x,'winrate 5']=f.create_winrate(past,5)
		x=x+1
		teams_avgs=teams_avgs.append(b)

	home=teams_avgs.iloc[[1]]
	away=teams_avgs.iloc[[2]]
	home=home.reset_index(drop=True)
	away=away.reset_index(drop=True)
	b=home.join(away,lsuffix='_home',rsuffix='_away')
	b=b.drop(del2,1)
	pred=clf.predict(b)
	print(games.loc[[game]],pred)
	preds.append(pred)

"""
df2log['mlp']=preds
df2log=df2log.sort_values('home')
log=log.append(df2log,sort=False)
log.to_csv(path2logs+'mlp_log.csv',index=False)
"""