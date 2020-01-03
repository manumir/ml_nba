import pandas as pd
import numpy as np
import os

path2og=os.getcwd()[:-4]

data=pd.read_csv(path2og+'train.csv')
data=data[['MIN_home','Team_home','Team_away','Game Date_home','Result']]

plac=pd.read_csv('plac_log.csv')

############  LINEAR REGRESSION  ############
lin=pd.read_csv('linear_log.csv')

data2calc=pd.DataFrame()
for date in list(set(list(lin['date'].values))):
	data2calc=data2calc.append(data.loc[data['Game Date_home']==date])
data2calc=data2calc.sort_values(['Game Date_home','Team_home'])
data2calc.reset_index(inplace=True,drop=True)

plac_lin=pd.DataFrame()
for date in list(set(list(data2calc['Game Date_home'].values))):
	plac_lin=plac_lin.append(plac.loc[plac['date']==date])
plac_lin=plac_lin.sort_values(['date','home'])
plac_lin.reset_index(inplace=True,drop=True)

# new_lin has the all the games minus the ones predicted and not
# have been played yet
new_lin=pd.DataFrame()
for date in list(set(list(data2calc['Game Date_home'].values))):
	new_lin=new_lin.append(lin.loc[lin['date']==date])
new_lin=new_lin.sort_values(['date','home'])
new_lin.reset_index(inplace=True,drop=True)

# check if logs are in the same order
for x in range(len(data2calc['Team_home'])):
	if data2calc.at[x,'Team_home'] != new_lin.at[x,'home'] or new_lin.at[x,'home'] != plac_lin.at[x,'home']:
		print('WRONG')
		break
#print(data2calc,'\n\n',new_lin,'\n\n',plac_lin)

count,spent=0,0
count_H,spent_H=0,0
count_A,spent_A=0,0
count_all=0
for x in range(len(data2calc['Team_home'])):
	if float(new_lin.at[x,'linear'][1:-1]) >= 0.49:
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

	if float(new_lin.at[x,'linear'][1:-1]) < 0.49:
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

################## MULTI LAYER PERCEPTRON ##############################
mlp=pd.read_csv('mlp_log.csv')

data2calc=pd.DataFrame()
for date in list(set(list(mlp['date'].values))):
	data2calc=data2calc.append(data.loc[data['Game Date_home']==date])
data2calc=data2calc.sort_values(['Game Date_home','Team_home'])
data2calc.reset_index(inplace=True,drop=True)

plac_mlp=pd.DataFrame()
for date in list(set(list(data2calc['Game Date_home'].values))):
	plac_mlp=plac_mlp.append(plac.loc[plac['date']==date])
plac_mlp=plac_mlp.sort_values(['date','home'])
plac_mlp.reset_index(inplace=True,drop=True)

new_mlp=pd.DataFrame()
for date in list(set(list(data2calc['Game Date_home'].values))):
	new_mlp=new_mlp.append(mlp.loc[mlp['date']==date])
new_mlp=new_mlp.sort_values(['date','home'])
new_mlp.reset_index(inplace=True,drop=True)

# check if logs are in the same order
for x in range(len(data2calc['Team_home'])):
	if data2calc.at[x,'Team_home'] != new_mlp.at[x,'home'] or new_mlp.at[x,'home'] != plac_mlp.at[x,'home']:
		print('WRONG')
		break
#print(data2calc,'\n\n',new_mlp,'\n\n',plac_mlp)

spent,count=0,0
spent_A,spent_H=0,0
count_A,count_H=0,0
count_all=0
for x in range(len(data2calc['Team_home'])):
	if round(float((new_mlp.at[x,'mlp'][1:-1]))) == 1:
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

	if round(float((new_mlp.at[x,'mlp'][1:-1]))) == 0:
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
# plac predictions
new_plac=pd.DataFrame()
for date in list(set(list(data['Game Date_home'].values))):
	new_plac=new_plac.append(plac.loc[plac['date']==date])
new_plac=new_plac.sort_values(['date','home'])
new_plac.reset_index(inplace=True,drop=True)

placpreds=[]
for x in range(len(new_plac)):
	if float(new_plac.at[x,'plac_H'])<float(new_plac.at[x,'plac_A']):
		placpreds.append(0)
	elif float(new_plac.at[x,'plac_H'])>float(new_plac.at[x,'plac_A']):
		placpreds.append(1)

# results
data2calc=pd.DataFrame()
for date in list(set(list(new_plac['date'].values))):
	data2calc=data2calc.append(data.loc[data['Game Date_home']==date])
data2calc=data2calc.sort_values(['Game Date_home','Team_home'])
data2calc.reset_index(inplace=True,drop=True)

count=0
for x in range(len(data2calc['Team_home'])):
	if placpreds[x]== 1:
		if data2calc.at[x,'MIN_home']==48:
			if data2calc.at[x,'Result']==1:
				count+=new_plac.at[x,'plac_A']
		count-=1
	if placpreds[x] == 0:
		if data2calc.at[x,'MIN_home']==48:
			if data2calc.at[x,'Result']==0:
				count+=new_plac.at[x,'plac_H']
		count-=1
print('placard return: {0:.4f}%'.format(count/len(new_plac) *100))
