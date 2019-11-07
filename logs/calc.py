import pandas as pd
import os

path2og=os.getcwd()[:-4]

rf=pd.read_csv('rf_log.csv')
lin=pd.read_csv('linear_log.csv')
plac=pd.read_csv('plac_log.csv')
data=pd.read_csv(path2og+'train.csv')

data2calc=data[:len(rf)].sort_values(['Game Date_home','Team_home'])
data2calc.reset_index(inplace=True,drop=True)

results=list(data2calc['Result'])

linpreds=[]
for x in lin['linear']:
	linpreds.append(round(float(x[1:-1])))

rfpreds=[]
for x in rf['rf']:
	rfpreds.append(round(float(x[1:-1])))

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
print('linear acc: ',count/len(results))

count=0
for x in range(len(results)):
	if (rfpreds[x])==(results[x]):
		count=count+1
print('rf acc: ',count/len(results))

count=0
for x in range(len(results)):
	if (placpreds[x])==(results[x]):
		count=count+1
print('plac acc: ',count/len(results))
