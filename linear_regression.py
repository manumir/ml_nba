#!/usr/bin/python3

import pandas as pd
import functions as f
from sklearn.linear_model import LinearRegression 

data=pd.read_csv('train.csv')
a=data.dropna()
a=a.drop(['Team_left','Match Up_left','Game Date_left','Team_right',
          'Match Up_right','Game Date_right','MIN_left','MIN_right',
          'W/L_left','W/L_right'],1)

corr=a.corr()['Result']
del2=[]
for x in corr.index:
  if abs(corr[x]) < 0.1:
    del2.append(x)

a=a.drop(del2,1)

train_dataset = a.sample(frac=0.85,random_state=19)#19,
test_dataset = a.drop(train_dataset.index)

#train_stats =train_dataset.describe()
#train_stats.pop('Result')
#train_stats = train_stats.transpose()

train_labels = train_dataset.pop('Result')
test_labels = test_dataset.pop('Result')

#def norm(x):
#  return (x - train_stats['mean']) / train_stats['std']
#normed_train_data = norm(train_dataset)
#normed_test_data = norm(test_dataset)

clf = LinearRegression()

clf.fit(train_dataset,train_labels)

preds=clf.predict(test_dataset)
print(f.acc(preds,test_labels))

