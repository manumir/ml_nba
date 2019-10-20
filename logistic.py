import pandas as pd
import functions as f
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
import joblib

data=pd.read_csv('train.csv')
a=data.dropna()
a=a.drop(['Team','Match Up','Game Date','Team_away',
           'Match Up_away','Game Date_away','MIN','MIN_away',
           'W/L','W/L_away'],1)

train_dataset = a.sample(frac=0.95,random_state=1)
test_dataset = a.drop(train_dataset.index)

train_labels = train_dataset.pop('Result')
test_labels = test_dataset.pop('Result')

clf = LogisticRegression(solver='liblinear')

train_dataset=preprocessing.normalize(train_dataset)
test_dataset=preprocessing.normalize(test_dataset)

train_dataset=preprocessing.scale(train_dataset)
test_dataset=preprocessing.scale(test_dataset)

clf.fit(train_dataset,train_labels)
#joblib.dump(clf,'Logistic.joblib')

acc=clf.score(test_dataset,test_labels)
preds=clf.predict(test_dataset)
print("\nacc: ",f.acc(preds,test_labels))

zeros,ones=0,0
for pred in preds:
  if round(pred)==1:
    ones+=1
  else:
    zeros+=1

print('\nlenght of test:',len(preds))
print('0s:',zeros/len(preds))
print('1s:',ones/len(preds))

