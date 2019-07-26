#!/usr/bin/env python

import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from pandas.plotting import scatter_matrix

#uncomment to train NN from b.csv
'''
file= pd.read_csv('b.csv')
file=file.drop(['Team','Match Up','Game Date'],1)
file=file.drop(['Unnamed: 0','MIN'],1)

#get file1
file1=file.loc[[1]]
x=3
while x < len(file.index):
    file1=file1.append(file.loc[[x]])
    x=x+2
    print(x)

#get file0
x=2
file0=file.loc[[0]]
while x < len(file.index):
    file0=file0.append(file.loc[[x]])
    x=x+2
    print(x)

#adjust file0 to same index as file1
file0=file0.set_index(file1.index)

a=file0.join(file1,lsuffix='_left',rsuffix='_right')#doesn't work because indexes don't correspond to one another
print('dataframes joined')

values_to_row=[]
for i in a.index:
    if a.loc[i,'W/L_left']=='W':
        values_to_row.append('0')#left team won
    else:
        values_to_row.append('1')#right team won
a['Result']=values_to_row
        
values_to_row=[]
for i in a.index:
    if a.loc[i,'H/A_left']=='home':
        values_to_row.append('0')#left tem is home
    else:
        values_to_row.append('1')#left team is away
a['Location']=values_to_row

a=a.drop(['W/L_left','W/L_right','H/A_left','H/A_right'],1)

print(a)


corr=a[a.columns].corr()['Result']
print('columns:' + str(len(a.columns)))
for i in corr.index:
  if abs(corr[i]) <0.07:
    a.pop(i)
print('columns:' + str(len(a.columns)))
a.to_csv('b1.csv')
'''
a=pd.read_csv('b1.csv')
#a=a.drop(['Unnamed: 0','Unnamed: 0.1_left','Unnamed: 0.1.1_left','Unnamed: 0.1.1.1_left','Unnamed: 0.1_right','Unnamed: 0.1.1_right','Unnamed: 0.1.1.1_right'],1)

a=a.drop('Unnamed: 0',1)
a=a.drop(['Unnamed: 0.1_left','Unnamed: 0.1_right'],1)
# unecessary because original data (30k rows are not calculated by new winrate script)
'''
# clean dataset of 12345% winrates
print(a.shape)
for i in range(len(a.index)):
    if a.loc[i]['winrate(69 games)_left']==12345 or a.loc[i]['winrate(69 games)_right']==12345:
        a=a.drop(a.loc[[i]].index)
print(a.shape)
'''
print(a.columns)
train_dataset = a.sample(frac=0.9)
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

print(normed_train_data.columns)
print(len(train_dataset.keys()))

def build_model():
    model = keras.Sequential([
    layers.Dense(41, input_shape=[len(train_dataset.keys())],activation='sigmoid'),
    layers.Dense(82,activation='sigmoid'),
    layers.Dense(1,activation='sigmoid'),
  ])
    model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])
    return model

model = build_model()
print(0)

early_stop = keras.callbacks.EarlyStopping(monitor='val_acc', patience=15)

# don't change checkpoint_path else, i fuck up the weights and the 67.4 accuracy

import os
checkpoint_path = "training_2/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create checkpoint callback
cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path, save_weights_only=True)

history = model.fit(normed_train_data, train_labels,validation_split=0.2, epochs=1500, callbacks=[early_stop])#,cp_callback])

print(model.evaluate(normed_test_data,test_labels)[1])
test_predictions = model.predict(normed_test_data)
print(test_predictions)

# i guess this is already done with model.evaluate, sad.
'''b=[]
for x in test_predictions:
    if x >= 0.5:
        b.append(int('1'))
    else:
        b.append(int('0'))
c=[]
for x in test_dataset.index:
    c.append(a.loc[x,'Result'])


count=0
divider=0
for x in range(len(b)):
    divider=divider+1
    if b[x]==c[x]:
        count=count+1
print((count/divider)*100)
'''

model.save('trying1.h5')
