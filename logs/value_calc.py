import pandas as pd
import datetime
import random

lin=pd.read_csv('linear_log.csv')
plac=pd.read_csv('plac_log.csv')

lin_preds=lin['linear']	

plac_H=plac['plac_H']
plac_A=plac['plac_A']

odd_H,odd_A=[],[]
for prediction in lin_preds:

	prob_H=1-float(prediction[1:-1])
	odd_H.append(1/prob_H)

	prob_A=1-prob_H
	odd_A.append(1/prob_A)

today=datetime.date.today()
today=today.strftime("%m/%d/%Y")

bet_home=pd.DataFrame()
date=[]
pred,myodd_H,plac_odd_H,lin_H,lin_A=[],[],[],[],[]
for i in range(len(plac_H)):
	if odd_H[i]-plac_H[i] < 0:
		if lin.at[i,'date'] == today:
			myodd_H.append(round(odd_H[i],2))
			plac_odd_H.append(plac_H[i])
			lin_H.append(lin.at[i,'home'])
			lin_A.append(lin.at[i,'away'])
			date.append(lin.at[i,'date'])
			pred.append(0)

bet_home['my odd']=myodd_H
bet_home['plac_odd']=plac_odd_H
bet_home['home']=lin_H
bet_home['away']=lin_A
bet_home['date']=date
bet_home['pred']=pred

# bets on away team
bet_away=pd.DataFrame()
date=[]
pred,myodd_A,plac_odd_A,lin_H,lin_A=[],[],[],[],[]
for i in range(len(plac_A)):	
	if odd_A[i]-plac_A[i] < 0:
		if lin.at[i,'date'] == today:
			myodd_A.append(round(odd_A[i],2))
			plac_odd_A.append(plac_A[i])
			lin_H.append(lin.at[i,'home'])
			lin_A.append(lin.at[i,'away'])
			date.append(lin.at[i,'date'])
			pred.append(1)

bet_away['my odd']=myodd_A
bet_away['plac_odd']=plac_odd_A
bet_away['home']=lin_H
bet_away['away']=lin_A
bet_away['date']=date
bet_away['pred']=pred

value_log=bet_away.append(bet_home)
print('value bets:',value_log)

# make 2 bets with 2 games each
home_bet=pd.DataFrame()
odd,home,away,date=[],[],[],[]
first_ix_H=random.randint(0,(len(bet_home)//2))
second_ix_H=random.randint((len(bet_home)//2),len(bet_home)) -1

first_odd_H=bet_home.at[first_ix_H,'plac_odd']
second_odd_H=bet_home.at[second_ix_H,'plac_odd']

odd.append(first_odd_H)
odd.append(second_odd_H)
home.append(bet_home.at[first_ix_H,'home'])
home.append(bet_home.at[second_ix_H,'home'])
away.append(bet_home.at[first_ix_H,'away'])
away.append(bet_home.at[second_ix_H,'away'])
date.append(bet_home.at[second_ix_H,'date'])
date.append(bet_home.at[first_ix_H,'date'])

home_bet['odd']=odd
home_bet['home']=home
home_bet['away']=away
home_bet['date']=date

# generate random indexes
first_ix_A=random.randint(0,(len(bet_away)//2))
second_ix_A=random.randint((len(bet_away)//2),len(bet_away)) -1

# get odds
first_odd_A=bet_away.at[first_ix_A,'plac_odd']
second_odd_A=bet_away.at[second_ix_A,'plac_odd']

# atribute home, away and date
away_bet=pd.DataFrame()
odd,home,away,date=[],[],[],[]
odd.append(first_odd_A)
odd.append(second_odd_A)
home.append(bet_away.at[first_ix_H,'home'])
home.append(bet_away.at[second_ix_H,'home'])
away.append(bet_away.at[first_ix_H,'away'])
away.append(bet_away.at[second_ix_H,'away'])
date.append(bet_away.at[first_ix_H,'date'])
date.append(bet_away.at[second_ix_H,'date'])

away_bet['odd']=odd
away_bet['home']=home
away_bet['away']=away
away_bet['date']=date

print(away_bet,'\n\n',home_bet)
