import pandas as pd
from sklearn.ensemble import RandomForestClassifier

data=pd.read_csv('train.csv')
a=data.dropna()

train_dataset = a.sample(frac=0.9)
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


clf = RandomForestClassifier(n_estimators=100, max_depth=None,min_samples_split=2, random_state=0)

clf.fit(train_dataset,train_labels)

acc=clf.score(test_dataset,test_labels)

print(acc)

