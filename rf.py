import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import functions as f

data=pd.read_csv('train.csv')
a=data.dropna()
a=a.drop(['Team_left','Match Up_left','Game Date_left','Team_right',
          'Match Up_right','Game Date_right','MIN_left','MIN_right',
          'W/L_left','W/L_right'],1)

train_dataset = a.sample(frac=0.85,random_state=1)
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

clf = RandomForestClassifier(n_estimators=1000,n_jobs=-1,random_state=0)

clf.fit(train_dataset,train_labels)
preds=clf.predict(test_dataset)
print(f.acc(preds,test_labels))

