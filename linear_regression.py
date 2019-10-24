import pandas as pd
import functions as f
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
import joblib

data=pd.read_csv('train.csv')
data=data.dropna()
data=data.drop(['Team','Match Up','Game Date','Team_away',
           'Match Up_away','Game Date_away','MIN','MIN_away',
           'W/L','W/L_away'],1)

corr=data.corr()['Result']
del2=[]
for x in corr.index:
  if abs(corr[x]) < 0.1:
    del2.append(x)
data=data.drop(del2,1)

print(data.columns)

clf=LinearRegression(n_jobs=-1)

#train_dataset = data.sample(frac=0.9,random_state=f.best_random_state(clf,data,list(range(350))))# 11,7
train_dataset = data.sample(frac=0.9,random_state=220)# 11,7
test_dataset = data.drop(train_dataset.index)

train_labels = train_dataset.pop('Result')
test_labels = test_dataset.pop('Result')

clf.fit(train_dataset,train_labels)

#joblib.dump(clf,'regression_linear.joblib')