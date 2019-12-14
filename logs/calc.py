import pandas as pd
import os

path2og=os.getcwd()[:-4]

plac=pd.read_csv('plac_log.csv')
plac=plac.sort_values(['date','home'])
plac.reset_index(inplace=True,drop=True)

rf=pd.read_csv('rf_log.csv')
rf=rf.sort_values(['date','home'])
rf.reset_index(inplace=True,drop=True)

lin=pd.read_csv('linear_log.csv')
lin=lin.sort_values(['date','home'])
lin.reset_index(inplace=True,drop=True)

mlp=pd.read_csv('mlp_log.csv')
mlp=mlp.sort_values(['date','home'])
mlp.reset_index(inplace=True,drop=True)

svm=pd.read_csv('svm_log.csv')
svm=svm.sort_values(['date','home'])
svm.reset_index(inplace=True,drop=True)

trees=pd.read_csv('trees_log.csv')
trees=trees.sort_values(['date','home'])
trees.reset_index(inplace=True,drop=True)

data=pd.read_csv(path2og+'train.csv')
data=data[['Team_home','Team_away','Game Date_home','Result']]

data2calc=pd.DataFrame()
for date in list(set(list(lin['date'].values))):
	data2calc=data2calc.append(data.loc[data['Game Date_home']==date])
data2calc=data2calc.sort_values(['Game Date_home','Team_home'])
data2calc.reset_index(inplace=True,drop=True)

results=list(data2calc['Result'])
""" # testing purposes
data2calc=data2calc[:5]
lin=lin[:5]
rf=rf[:5]
plac=plac[:5]
print(data2calc,rf,lin,plac)
"""
linpreds=[]
#zeros=0
for x in lin['linear']:
	if float(x[1:-1]) <0.49:
		linpreds.append(0)
#		zeros=zeros+1
	else:
		linpreds.append(1)
	#linpreds.append(round(float(x[1:-1])))

#testing if a lot biased towards home
#print(zeros/(len(linpreds)))

rfpreds=[]
for x in rf['rf']:
	rfpreds.append(round(float(x[1:-1])))

mlp_preds=[]
for x in mlp['mlp']:
	mlp_preds.append(round(float(x[1:-1])))

svm_preds=[]
for x in svm['svm']:
	svm_preds.append(round(float(x[1:-1])))

trees_preds=[]
for x in trees['trees']:
	trees_preds.append(round(float(x[1:-1])))

placpreds=[]
for x in range(len(plac)):
	if float(plac.at[x,'plac_H'])<float(plac.at[x,'plac_A']):
		placpreds.append(0)
	elif float(plac.at[x,'plac_H'])>float(plac.at[x,'plac_A']):
		placpreds.append(1)

count=0
for x in range(len(results)):
	if (linpreds[x])==(results[x]):
		count=count+1
print('\nlinear acc:',count/len(results),'right:',count,'total:',len(results))

count=0
for x in range(len(results)):
	if (rfpreds[x])==(results[x]):
		count=count+1
print('rf acc:',count/len(results),'right:',count,'total:',len(results))

count=0
for x in range(len(results)):
	if (placpreds[x])==(results[x]):
		count=count+1
print('plac acc:',count/len(results),'right:',count,'total:',len(results))

## mlp accuracy
data2calc_mlp=pd.DataFrame()
for date in list(set(list(mlp['date'].values))):
	data2calc_mlp=data2calc_mlp.append(data.loc[data['Game Date_home']==date])
data2calc_mlp=data2calc_mlp.sort_values(['Game Date_home','Team_home'])
data2calc_mlp.reset_index(inplace=True,drop=True)

mlp_results=list(data2calc_mlp['Result'])

count=0
for x in range(len(mlp_results)):
	if (mlp_preds[x])==(mlp_results[x]):
		count=count+1
print('\nmlp acc:',count/len(mlp_results),'right:',count,'total:',len(mlp_results))

# placard on the mlp games
plac_mlp=pd.DataFrame()
for date in list(set(list(mlp['date'].values))):
	plac_mlp=plac_mlp.append(plac.loc[plac['date']==date])
plac_mlp=plac_mlp.sort_values(['date','home'])
plac_mlp.reset_index(inplace=True,drop=True)

placpreds_mlp=[]
for x in range(len(plac_mlp)):
	if float(plac_mlp.at[x,'plac_H'])<float(plac_mlp.at[x,'plac_A']):
		placpreds_mlp.append(0)
	elif float(plac_mlp.at[x,'plac_H'])>float(plac_mlp.at[x,'plac_A']):
		placpreds_mlp.append(1)

count=0
for x in range(len(mlp_results)):
	if (placpreds_mlp[x])==(mlp_results[x]):
		count=count+1
	""" # testing
	else:
		print(data2calc_mlp.at[x,'Team_home'],data2calc_mlp.at[x,'Team_away'],data2calc_mlp.at[x,'Result'],placpreds[x])
	"""		
print('plac acc_mlp:',count/len(mlp_results),'right:',count,'total:',len(mlp_results),'\n')

################### FIX THESE TWO, ADD XGB ###############
count=0
svm_results=results[-(len(svm_preds)):]
for x in range(len(svm_results)):
	if (svm_preds[x])==(svm_results[x]):
		count=count+1
print('svm acc:',count/len(svm_results),'right:',count,'total:',len(svm_results))

count=0
trees_results=results[-(len(trees_preds)):]
for x in range(len(trees_results)):
	if (trees_preds[x])==(trees_results[x]):
		count=count+1
print('trees acc:',count/len(trees_results),'right:',count,'total:',len(trees_results),'\n')
##########################################################