#!/usr/bin/python3

import os
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
import functions as f

curr_path=os.getcwd()
path2data=curr_path[:-6]

a=pd.read_csv(path2data+'train.csv')
a=a.dropna()
a=a.drop(['Team_home','Match Up_home','Game Date_home','Team_away',
           'Match Up_away','Game Date_away','MIN_home','MIN_away',
           'W/L_home','W/L_away'],1)

corr=a.corr()['Result']
del2=[]
for x in corr.index:
  if abs(corr[x]) < 0.1:
    del2.append(x)
data=a.drop(del2,1)

# split data into train and test sets
Y=data.pop('Result')
X=data
x_train,x_test,y_train,y_test = train_test_split(X, Y, test_size=0.01, random_state=12)

def build_model():
    model = keras.Sequential([
    layers.Dense(X.shape[1],input_shape=[len(X.keys())],activation='sigmoid'),
    layers.Dense(1,activation='sigmoid'),
  ])
    model.compile(optimizer='adam',
              loss='mse',
              metrics=['accuracy'])
    return model

model = build_model()
early_stop = keras.callbacks.EarlyStopping(monitor='val_acc', patience=15)
history = model.fit(x_train,y_train,validation_split=0.2, epochs=500, callbacks=[early_stop])

acc= model.evaluate(x_test,y_test)
print("\nacc: ",acc,'\n')

#model.save('1.h5')
