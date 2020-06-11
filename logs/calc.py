import pandas as pd
import os

path2og=os.getcwd()[:-4]

data=pd.read_csv(path2og+'train.csv')
data=data[['Team_home','Team_away','Game Date_home','Result']]

########################### LIN,RF,PLAC ACCURACY ##########################
#rf=pd.read_csv('rf_log.csv')
lin=pd.read_csv('linear_log.csv')
plac=pd.read_csv('plac_log.csv')

data2calc_lin=pd.DataFrame()
for date in list(set(list(lin['date'].values))):
	data2calc_lin=data2calc_lin.append(data.loc[data['Game Date_home']==date])
data2calc_lin=data2calc_lin.sort_values(['Game Date_home','Team_home'])
data2calc_lin.reset_index(inplace=True,drop=True)

plac_lin=pd.DataFrame()
for date in list(set(list(data2calc_lin['Game Date_home'].values))):
	plac_lin=plac_lin.append(plac.loc[plac['date']==date])
plac_lin=plac_lin.sort_values(['date','home'])
plac_lin.reset_index(inplace=True,drop=True)

placpreds=[]
for x in range(len(plac_lin)):
	if float(plac_lin.at[x,'plac_H'])<float(plac_lin.at[x,'plac_A']):
		placpreds.append(0)
	elif float(plac_lin.at[x,'plac_H'])>float(plac_lin.at[x,'plac_A']):
		placpreds.append(1)
"""
new_rf=pd.DataFrame()
for date in list(set(list(data2calc_lin['Game Date_home'].values))):
	new_rf=new_rf.append(rf.loc[rf['date']==date])
new_rf=new_rf.sort_values(['date','home'])
new_rf.reset_index(inplace=True,drop=True)
"""
new_lin=pd.DataFrame()
for date in list(set(list(data2calc_lin['Game Date_home'].values))):
	new_lin=new_lin.append(lin.loc[lin['date']==date])
new_lin=new_lin.sort_values(['date','home'])
new_lin.reset_index(inplace=True,drop=True)

linpreds=[]
for x in new_lin['linear']:
	if float(x[1:-1]) <0.49:
		linpreds.append(0)
	else:
		linpreds.append(1)
	#linpreds.append(round(float(x[1:-1])))

results=list(data2calc_lin['Result'])

# check if logs are in the same order
for x in range(len(data2calc_lin['Team_home'])):
	if data2calc_lin.at[x,'Team_home'] != new_lin.at[x,'home'] or new_lin.at[x,'home'] != plac_lin.at[x,'home']:
		print('WRONG')
		break

count=0
for x in range(len(results)):
	if (linpreds[x])==(results[x]):
		count=count+1
print('\nlinear acc:',count/len(results),'right:',count,'total:',len(results))
"""
count=0
for x in range(len(results)):
	if round(float(new_rf.at[x,'rf'][1:-1]))==(results[x]):
		count=count+1
print('rf acc:',count/len(results),'right:',count,'total:',len(results))
"""
count=0
for x in range(len(results)):
	if (placpreds[x])==(results[x]):
		count=count+1
print('plac acc:',count/len(results),'right:',count,'total:',len(results))


########################## MLP,PLAC ######################################
mlp=pd.read_csv('mlp_log.csv')

data2calc_mlp=pd.DataFrame()
for date in list(set(list(mlp['date'].values))):
	data2calc_mlp=data2calc_mlp.append(data.loc[data['Game Date_home']==date])
data2calc_mlp=data2calc_mlp.sort_values(['Game Date_home','Team_home'])
data2calc_mlp.reset_index(inplace=True,drop=True)

mlp_results=list(data2calc_mlp['Result'])

new_mlp=pd.DataFrame()
for date in list(set(list(data2calc_mlp['Game Date_home'].values))):
	new_mlp=new_mlp.append(mlp.loc[mlp['date']==date])
new_mlp=new_mlp.sort_values(['date','home'])
new_mlp.reset_index(inplace=True,drop=True)

count=0
for x in range(len(mlp_results)):
	if round(float(new_mlp.at[x,'mlp'][1:-1]))==(mlp_results[x]):
		count=count+1
print('\nmlp acc:',count/len(mlp_results),'right:',count,'total:',len(mlp_results))

# placard on the mlp games
plac_mlp=pd.DataFrame()
for date in list(set(list(new_mlp['date'].values))):
	plac_mlp=plac_mlp.append(plac.loc[plac['date']==date])
plac_mlp=plac_mlp.sort_values(['date','home'])
plac_mlp.reset_index(inplace=True,drop=True)

placpreds_mlp=[]
for x in range(len(plac_mlp)):
	if float(plac_mlp.at[x,'plac_H'])<float(plac_mlp.at[x,'plac_A']):
		placpreds_mlp.append(0)
	elif float(plac_mlp.at[x,'plac_H'])>float(plac_mlp.at[x,'plac_A']):
		placpreds_mlp.append(1)

# check if logs are in the same order
for x in range(len(data2calc_mlp['Team_home'])):
	if data2calc_mlp.at[x,'Team_home'] != new_mlp.at[x,'home']:
		print('WRONG 0')
	if new_mlp.at[x,'home'] != plac_mlp.at[x,'home']:
		print('WRONG 1')
		break

count=0
for x in range(len(mlp_results)):
	if (placpreds_mlp[x])==(mlp_results[x]):
		count=count+1
	""" # testing
	else:
		print(data2calc_mlp.at[x,'Team_home'],data2calc_mlp.at[x,'Team_away'],data2calc_mlp.at[x,'Result'],placpreds[x])
	"""		
print('plac acc_mlp:',count/len(mlp_results),'right:',count,'total:',len(mlp_results))


"""
svm=pd.read_csv('svm_log.csv')
svm=svm.sort_values(['date','home'])
svm.reset_index(inplace=True,drop=True)

trees=pd.read_csv('trees_log.csv')
trees=trees.sort_values(['date','home'])
trees.reset_index(inplace=True,drop=True)

xgb=pd.read_csv('xgb_log.csv')
xgb=xgb.sort_values(['date','home'])
xgb.reset_index(inplace=True,drop=True)

########################## SVM,TREES,PLAC ######################################
# svm
data2calc_svm=pd.DataFrame()
for date in list(set(list(svm['date'].values))):
	data2calc_svm=data2calc_svm.append(data.loc[data['Game Date_home']==date])
data2calc_svm=data2calc_svm.sort_values(['Game Date_home','Team_home'])
data2calc_svm.reset_index(inplace=True,drop=True)

svm_results=list(data2calc_svm['Result'])

count=0
for x in range(len(svm_results)):
	if round(float(svm.at[x,'svm'][1:-1]))==(svm_results[x]):
		count=count+1
print('\nsvm acc:',count/len(svm_results),'right:',count,'total:',len(svm_results))

# trees
data2calc_trees=pd.DataFrame()
for date in list(set(list(trees['date'].values))):
	data2calc_trees=data2calc_trees.append(data.loc[data['Game Date_home']==date])
data2calc_trees=data2calc_trees.sort_values(['Game Date_home','Team_home'])
data2calc_trees.reset_index(inplace=True,drop=True)

trees_results=list(data2calc_trees['Result'])

count=0
for x in range(len(trees_results)):
	if round(float(trees.at[x,'trees'][1:-1]))==(trees_results[x]):
		count=count+1
print('trees acc:',count/len(trees_results),'right:',count,'total:',len(trees_results))

# placard on the svm/tree games
plac_svm=pd.DataFrame()
for date in list(set(list(svm['date'].values))):
	plac_svm=plac_svm.append(plac.loc[plac['date']==date])
plac_svm=plac_svm.sort_values(['date','home'])
plac_svm.reset_index(inplace=True,drop=True)

placpreds_svm=[]
for x in range(len(plac_svm)):
	if float(plac_svm.at[x,'plac_H'])<float(plac_svm.at[x,'plac_A']):
		placpreds_svm.append(0)
	elif float(plac_svm.at[x,'plac_H'])>float(plac_svm.at[x,'plac_A']):
		placpreds_svm.append(1)

count=0
for x in range(len(svm_results)):
	if (placpreds_svm[x])==(svm_results[x]):
		count=count+1
	# testing
	#else:
	#	print(data2calc_mlp.at[x,'Team_home'],data2calc_mlp.at[x,'Team_away'],data2calc_mlp.at[x,'Result'],placpreds[x])
			
print('plac acc_svm/tree:',count/len(svm_results),'right:',count,'total:',len(svm_results),'\n')



####################### XGBOOST,PLAC ####################################
data2calc_xgb=pd.DataFrame()
for date in list(set(list(xgb['date'].values))):
	data2calc_xgb=data2calc_xgb.append(data.loc[data['Game Date_home']==date])
data2calc_xgb=data2calc_xgb.sort_values(['Game Date_home','Team_home'])
data2calc_xgb.reset_index(inplace=True,drop=True)

xgb_results=list(data2calc_xgb['Result'])

count=0
for x in range(len(xgb_results)):
	if round(float(xgb.at[x,'xgb'][1:-1]))==(xgb_results[x]):
		count=count+1
print('xgb acc:',count/len(xgb_results),'right:',count,'total:',len(xgb_results))

# placard on the xgb games
plac_xgb=pd.DataFrame()
for date in list(set(list(xgb['date'].values))):
	plac_xgb=plac_xgb.append(plac.loc[plac['date']==date])
plac_xgb=plac_xgb.sort_values(['date','home'])
plac_xgb.reset_index(inplace=True,drop=True)

placpreds_xgb=[]
for x in range(len(plac_xgb)):
	if float(plac_xgb.at[x,'plac_H'])<float(plac_xgb.at[x,'plac_A']):
		placpreds_xgb.append(0)
	elif float(plac_xgb.at[x,'plac_H'])>float(plac_xgb.at[x,'plac_A']):
		placpreds_xgb.append(1)

count=0
for x in range(len(xgb_results)):
	if (placpreds_xgb[x])==(xgb_results[x]):
		count=count+1
	# testing
	#else:
	#	print(data2calc_mlp.at[x,'Team_home'],data2calc_mlp.at[x,'Team_away'],data2calc_mlp.at[x,'Result'],placpreds[x])
			
print('plac acc_xgb:',count/len(xgb_results),'right:',count,'total:',len(xgb_results),'\n')

########################### see accuracy by team #####################################
import matplotlib.pyplot as plt
teams=['MEM', 'HOU', 'BKN', 'BOS', 'LAC', 'NOP', 'SAC', 'POR', 'DET', 'UTA', 'CHA', 'SAS', 'WAS', 'TOR','DEN','MIL', 'ATL','GSW', 'DAL', 'ORL', 'PHI', 'NYK', 'LAL', 'CLE', 'OKC', 'MIN', 'CHI', 'MIA', 'PHX', 'IND']
d={}
for team in teams:
	d[team]=0
count=0
new_lin['linear']=linpreds
for x in range(len(results)):
	if (new_lin.at[x,'linear'])==(results[x]):
		d[new_lin.at[x,'home']]=d[new_lin.at[x,'home']]+1
		d[new_lin.at[x,'away']]=d[new_lin.at[x,'away']]+1
		count=count+1

e={}
for team in teams:
	e[team]=0
count=0
for x in range(len(results)):
	e[new_lin.at[x,'home']]=e[new_lin.at[x,'home']]+1
	e[new_lin.at[x,'away']]=e[new_lin.at[x,'away']]+1

for team in teams:
	d[team]=d[team]/e[team]

plt.scatter(list(d.keys()),list(d.values()))
plt.show()
"""
