import pandas as pd
import os

path2og=os.getcwd()[:-4]

plac=pd.read_csv('plac_log.csv')
rf=pd.read_csv('rf_log.csv')
lin=pd.read_csv('linear_log.csv')
mlp=pd.read_csv('mlp_log.csv')
svm=pd.read_csv('svm_log.csv')
trees=pd.read_csv('trees_log.csv')

data=pd.read_csv(path2og+'train.csv')
data=data[['Team_home','Team_away','Game Date_home','Result']]

data2calc=pd.DataFrame()
for date in list(set(list(lin['date'].values))):
	data2calc=data2calc.append(data.loc[data['Game Date_home']==date])

data2calc=data2calc.sort_values(['Game Date_home','Team_home'])
data2calc.reset_index(inplace=True,drop=True)

rf=rf.sort_values(['date','home'])
rf.reset_index(inplace=True,drop=True)

lin=lin.sort_values(['date','home'])
lin.reset_index(inplace=True,drop=True)

mlp=mlp.sort_values(['date','home'])
mlp.reset_index(inplace=True,drop=True)

svm=svm.sort_values(['date','home'])
svm.reset_index(inplace=True,drop=True)

trees=trees.sort_values(['date','home'])
trees.reset_index(inplace=True,drop=True)

plac=plac.sort_values(['date','home'])
plac.reset_index(inplace=True,drop=True)

""" testing purposes
data2calc=data2calc[:5]
lin=lin[:5]
rf=rf[:5]
plac=plac[:5]
print(data2calc,rf,lin,plac)
"""
results=list(data2calc['Result'])

linpreds=[]
zeros=0
for x in lin['linear']:
	if float(x[1:-1]) <0.51:
		linpreds.append(0)
		zeros=zeros+1
	else:
		linpreds.append(1)
	#linpreds.append(round(float(x[1:-1])))

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
print('linear acc: ',count/len(results),'right: ',count,'total: ',len(results))

count=0
mlp_results=results[-(len(mlp_preds)):]
for x in range(len(mlp_results)):
	if (mlp_preds[x])==(mlp_results[x]):
		count=count+1
print('mlp acc: ',count/len(mlp_results),'right: ',count,'total: ',len(mlp_results))

count=0
svm_results=results[-(len(svm_preds)):]
for x in range(len(svm_results)):
	if (svm_preds[x])==(svm_results[x]):
		count=count+1
print('svm acc: ',count/len(svm_results),'right: ',count,'total: ',len(svm_results))

count=0
trees_results=results[-(len(trees_preds)):]
for x in range(len(trees_results)):
	if (trees_preds[x])==(trees_results[x]):
		count=count+1
print('trees acc: ',count/len(trees_results),'right: ',count,'total: ',len(trees_results))

count=0
for x in range(len(results)):
	if (rfpreds[x])==(results[x]):
		count=count+1
print('rf acc: ',count/len(results),'right: ',count,'total: ',len(results))

count=0
for x in range(len(results)):
	if (placpreds[x])==(results[x]):
		count=count+1
print('plac acc: ',count/len(results),'right: ',count,'total: ',len(results))

count=0
for x in range(len(mlp_preds)):
	if results[-len(mlp_preds):][x]==placpreds[-len(mlp_preds):][x]:
		count+=1
print('plac(len(mlp))',count,count/(len(mlp_preds)) *100)
