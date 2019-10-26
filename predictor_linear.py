import pandas as pd
from sklearn import preprocessing
import joblib

data=pd.read_csv('data.csv')

c2_pred=['FG%', '+/-', 'winrate 30', 'winrate 6', 'FG%_away', '+/-_away',
		'winrate 30_away', 'winrate 6_away']

df=pd.DataFrame()
home,away,pred=[],[],[]

games=pd.read_csv('games.csv')
for game in list(range(len(games))):
	home=data.loc[data['Team']==games.at[game,'home']]
	away=data.loc[data['Team']==games.at[game,'away']]
	home=home.reset_index(drop=True)
	away=away.reset_index(drop=True)
	home=home.loc[[game]]
	away=away.loc[[game]]
	
	home=home[['PTS','FGM','FGA','FG%','3PM','3PA','3P%','FTM','FTA','FT%',
	'OREB','DREB','REB','AST','TOV','STL','BLK','PF','+/-','winrate 30','winrate 6']]
	away=away[['PTS','FGM','FGA','FG%','3PM','3PA','3P%','FTM','FTA','FT%',
	'OREB','DREB','REB','AST','TOV','STL','BLK','PF','+/-','winrate 30','winrate 6']]
	
	b=home.join(away,rsuffix='_away')

	model=joblib.load('regression_linear.joblib')
	b=b[c2_pred] # only necessary when model is linear regression
	
	#print(b)
	pred.append(model.predict(b))
	#print(games.at[game,'home'],games.at[game,'away'],model.predict(b))

name='linear_log.csv'
log=pd.read_csv(name)
df['home']=games['home']
df['away']=games['away']
df['pred']=pred
log=log.append(df,sort=False)
log.to_csv(name,index=False)
