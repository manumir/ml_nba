import pandas as pd

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

for i in range(len(plac_H)):
	if odd_H[i]-plac_H[i] < 0:
		print(odd_H[i],plac_H[i],lin.at[i,'home'],lin.at[i,'date'])