# tester for duplicated rows

import pandas as pd

data=pd.read_csv('train.csv')

data['dup']=data.duplicated()

print(data[data['dup']==True])
