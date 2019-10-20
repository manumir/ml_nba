import pandas as pd

data=pd.read_csv('train.csv')

data=data.dropna()

print(data.corr()['Result'])
