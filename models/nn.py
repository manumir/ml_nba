#!/usr/bin/python3

import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import functions as f

a=pd.read_csv('train.csv')
a=a.dropna()
a=a.drop(['Team','Match Up','Game Date','Team_away',
           'Match Up_away','Game Date_away','MIN','MIN_away',
           'W/L','W/L_away'],1)

corr=a.corr()['Result']
del2=[]
for x in corr.index:
  if abs(corr[x]) < 0.1:
    del2.append(x)

a=a.drop(del2,1)

train_dataset = a.sample(frac=0.95,random_state=5)
test_dataset = a.drop(train_dataset.index)

train_stats =train_dataset.describe()
train_stats.pop('Result')
train_stats = train_stats.transpose()

train_labels = train_dataset.pop('Result')
test_labels = test_dataset.pop('Result')

def norm(x):
  return (x - train_stats['mean']) / train_stats['std']
normed_train_data = norm(train_dataset)
normed_test_data = norm(test_dataset)

print(len(train_dataset.keys()))

def build_model():
    model = keras.Sequential([
    layers.Dense(train_dataset.shape[1],input_shape=[len(train_dataset.keys())],activation='sigmoid'),
    layers.Dense(train_dataset.shape[1],activation='sigmoid'),
    layers.Dense(1,activation='sigmoid'),
  ])
    model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])
    return model

model = build_model()
early_stop = keras.callbacks.EarlyStopping(monitor='val_acc', patience=20)
history = model.fit(normed_train_data, train_labels,validation_split=0.2, epochs=500, callbacks=[early_stop])

acc= model.evaluate(normed_test_data,test_labels)
print("\nacc: ",acc,'\n')

#model.save('1.h5')
