import pandas as pd
import numpy as np
import os

path2og=os.getcwd()[:-4]
#games=pd.read_csv(path2og+'games.csv') i don't think this is needed (data2calc has right len)

plac=pd.read_csv('plac_log.csv')
plac=plac.sort_values(['date','home'])
plac.reset_index(inplace=True,drop=True)

lin=pd.read_csv('linear_log.csv')
lin=lin.sort_values(['date','home'])
lin.reset_index(inplace=True,drop=True)

mlp=pd.read_csv('mlp_log.csv')
mlp=mlp.sort_values(['date','home'])
mlp.reset_index(inplace=True,drop=True)

data=pd.read_csv(path2og+'train.csv')
data=data[:len(plac)]
data=data[['MIN_home','Team_home','Team_away','Game Date_home','Result']]

############  LINEAR REGRESSION  ############
data2calc=pd.DataFrame()
for date in list(set(list(lin['date'].values))):
	data2calc=data2calc.append(data.loc[data['Game Date_home']==date])
data2calc=data2calc.sort_values(['Game Date_home','Team_home'])
data2calc.reset_index(inplace=True,drop=True)

plac_lin=pd.DataFrame()
for date in list(set(list(lin['date'].values))):
	plac_lin=plac_lin.append(plac.loc[plac['date']==date])
plac_lin=plac_lin.sort_values(['date','home'])
plac_lin.reset_index(inplace=True,drop=True)

# check if logs are in the same order
for x in range(len(data2calc['Team_home'])):
	if data2calc.at[x,'Team_home'] != lin.at[x,'home']:
		print('wrong')

count,spent=0,0
count_H,spent_H=0,0
count_A,spent_A=0,0
count_all=0
for x in range(len(data2calc['Team_home'])):
	if float(lin.at[x,'linear'][1:-1]) >= 0.49:
		if plac_lin.at[x,'plac_A']>plac_lin.at[x,'plac_H']:
#			print(lin.at[x,'home'],lin.at[x,'away'])
			if data2calc.at[x,'MIN_home']==48 and data2calc.at[x,'Result']==1:
#					print('disagreed i said',lin.at[x,'away'],data2calc.at[x,'Game Date_home'],plac_lin.at[x,'plac_A'])
					count+=plac_lin.at[x,'plac_A']
					count_A+=plac_lin.at[x,'plac_A']
			count-=1
			spent+=1
			count_A-=1
			spent_A+=1
		if data2calc.at[x,'MIN_home']==48 and data2calc.at[x,'Result']==1:
			count_all+=plac_lin.at[x,'plac_A']

	if float(lin.at[x,'linear'][1:-1]) < 0.49:
		if plac_lin.at[x,'plac_H']>plac_lin.at[x,'plac_A']:
#			print(lin.at[x,'home'],lin.at[x,'away'])
			if data2calc.at[x,'MIN_home']==48 and data2calc.at[x,'Result']==0:
#					print('disagreed i said',lin.at[x,'home'],data2calc.at[x,'Game Date_home'],plac_lin.at[x,'plac_H'])
					count+=plac_lin.at[x,'plac_H']
					count_H+=plac_lin.at[x,'plac_H']
			count-=1
			spent+=1
			count_H-=1
			spent_H+=1

		if data2calc.at[x,'MIN_home']==48 and data2calc.at[x,'Result']==0:
			count_all+=plac_lin.at[x,'plac_H']

print('total_H: {:.2f} spent_H: {}'.format(count_H,spent_H))
print('linear return on home: {:.4f}%\n'.format(count_H/spent_H *100))

print('total_A: {:.2f} spent_A: {}'.format(count_A,spent_A))
print('linear return on away: {:.4f}%\n'.format(count_A/spent_A *100))

print('total: {:.2f} spent: {}'.format(count,spent))
print('linear return disagreed: {:.4f}%\n'.format(count/spent *100))

print('total_H: {:.2f} spent_H: {}'.format(count_all,len(data2calc)))
print('linear return on ALL games: {:.4f}%\n\n'.format((count_all-len(data2calc))/len(data2calc) *100))
## MULTI LAYER PERCEPTRON
data2calc=pd.DataFrame()
for date in list(set(list(mlp['date'].values))):
	data2calc=data2calc.append(data.loc[data['Game Date_home']==date])
data2calc=data2calc.sort_values(['Game Date_home','Team_home'])
data2calc.reset_index(inplace=True,drop=True)

plac_mlp=pd.DataFrame()
for date in list(set(list(mlp['date'].values))):
	plac_mlp=plac_mlp.append(plac.loc[plac['date']==date])
plac_mlp=plac_mlp.sort_values(['date','home'])
plac_mlp.reset_index(inplace=True,drop=True)
#plac_mlp=plac_mlp[:-(len(games))] check top note this file

#print(data2calc,mlp,plac_mlp)

# check if logs are in the same order
for x in range(len(data2calc['Team_home'])):
	if data2calc.at[x,'Team_home'] != mlp.at[x,'home']:
		print('wrong')

spent,count=0,0
spent_A,spent_H=0,0
count_A,count_H=0,0
count_all=0
for x in range(len(data2calc['Team_home'])):
	if round(float((mlp.at[x,'mlp'][1:-1]))) == 1:
		if plac_mlp.at[x,'plac_A']>plac_mlp.at[x,'plac_H']:
#			print(mlp.at[x,'home'],mlp.at[x,'away'])
			if data2calc.at[x,'MIN_home']==48 and data2calc.at[x,'Result']==1:
#					print('disagreed i said',mlp.at[x,'away'],data2calc.at[x,'Game Date_home'],plac_mlp.at[x,'plac_A'])
					count+=plac_mlp.at[x,'plac_A']
					count_A+=plac_mlp.at[x,'plac_A']
			count-=1
			spent+=1
			count_A-=1
			spent_A+=1
	
		if data2calc.at[x,'MIN_home']==48 and data2calc.at[x,'Result']==1:
			count_all+=plac_mlp.at[x,'plac_A']

	if round(float((mlp.at[x,'mlp'][1:-1]))) == 0:
		if plac_mlp.at[x,'plac_H']>plac_mlp.at[x,'plac_A']:
#			print(mlp.at[x,'home'],mlp.at[x,'away'])
			if data2calc.at[x,'MIN_home']==48 and data2calc.at[x,'Result']==0:
#					print('disagreed i said',mlp.at[x,'home'],data2calc.at[x,'Game Date_home'],plac_mlp.at[x,'plac_H'])
					count+=plac_mlp.at[x,'plac_H']
					count_H+=plac_mlp.at[x,'plac_H']
			count-=1
			spent+=1
			count_H-=1
			spent_H+=1

		if data2calc.at[x,'MIN_home']==48 and data2calc.at[x,'Result']==0:
			count_all+=plac_mlp.at[x,'plac_H']

print('total_H: {:.2f} spent_H: {}'.format(count_H,spent_H))
print('perceptron return on home: {:.4f}%\n'.format(count_H/spent_H *100))

print('total_A: {:.2f} spent_A: {}'.format(count_A,spent_A))
print('perceptron return on away: {:.4f}%\n'.format(count_A/spent_A *100))

print('total: {:.2f} spent: {}'.format(count,spent))
print('perceptron return disagreed: {:.4f}%\n'.format(count/spent *100))

print('total_H: {:.2f} spent_H: {}'.format(count_all,len(data2calc)))
print('perceptron return on ALL games: {:.4f}%\n\n'.format((count_all-len(data2calc))/len(data2calc) *100))
################ placard ##################
placpreds=[]
for x in range(len(plac)):
	if float(plac.at[x,'plac_H'])<float(plac.at[x,'plac_A']):
		placpreds.append(0)
	elif float(plac.at[x,'plac_H'])>float(plac.at[x,'plac_A']):
		placpreds.append(1)

# sort
data2calc=pd.DataFrame()
for date in list(set(list(plac['date'].values))):
	data2calc=data2calc.append(data.loc[data['Game Date_home']==date])
data2calc=data2calc.sort_values(['Game Date_home','Team_home'])
data2calc.reset_index(inplace=True,drop=True)

count=0
for x in range(len(data2calc['Team_home'])):
	if placpreds[x]== 1:
		if data2calc.at[x,'MIN_home']==48:
			if data2calc.at[x,'Result']==1:
				count+=plac.at[x,'plac_A']
		count-=1
	if placpreds[x] == 0:
		if data2calc.at[x,'MIN_home']==48:
			if data2calc.at[x,'Result']==0:
				count+=plac.at[x,'plac_H']
		count-=1
print('placard return: {0:.4f}%'.format(count/len(plac) *100))
