import pandas as pd
import functions as f
import os
import xgboost as xgb
from sklearn.model_selection import train_test_split

curr_path=os.getcwd()
path2data=curr_path[:-6]
path2logs=curr_path[:-6]+'\\logs\\'
log=pd.read_csv(path2logs+'xgb_log.csv')

# load data
data=pd.read_csv(path2data+'train.csv')
data=data.dropna()
data=data.drop(['Team_home','Match Up_home','Game Date_home','Team_away',
           'Match Up_away','Game Date_away','MIN_home','MIN_away',
           'W/L_home','W/L_away'],1)
Y=data.pop('Result')
X=data

# split data into train and test sets
X_train,X_test,y_train,y_test = train_test_split(X, Y, test_size=0.01, random_state=7)

# fit model no training data
model = xgb.XGBRegressor()
model.fit(X_train, y_train)

# make predictions for test data
y_pred = model.predict(X_test)

print('zeros:',f.get0and1(y_pred))
# evaluate predictions
accuracy = f.acc(y_test,y_pred)
print("Accuracy: %.2f%%" % (accuracy * 100.0))

preds=model.predict
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
for game in list(range(len(games))):
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
		b.at[x,'fatigue']=int(f.fatigue(past))
		teams_avgs=teams_avgs.append(b)
		x=x+1

	home=teams_avgs.iloc[[1]]
	away=teams_avgs.iloc[[2]]
	home=home.reset_index(drop=True)
	away=away.reset_index(drop=True)
	b=home.join(away,lsuffix='_home',rsuffix='_away')
	pred=model.predict(b)
	print(games.loc[[game]],pred)
	preds.append(pred)

df2log['xgb']=preds
df2log=df2log.sort_values('home')
log=log.append(df2log,sort=False)
log.to_csv(path2logs+'xgb_log.csv',index=False)
