#! /usr/bin/env python3

import pandas as pd
import os

path=os.getcwd()
file2=open(path+'/files/my predicts2.csv','w')
file2.write('Home,Away,predicts\n')
file2.close()

file1=pd.read_csv('b.csv')
file1.pop('MIN')
file1.pop('Unnamed: 0')
print(file1.columns)

auto=pd.read_csv('games.csv')

x=0
while x < len(auto.index):
####################################### NEED TO GET RID OF THIS SPAGETHI CODE #######################
    home=auto.iloc[x]['home']
    data_home=file1.loc[file1['Team'] ==home].iloc[[0]]
    data_home=data_home.drop(['Team','Match Up','Game Date'],1)
    
    away=auto.iloc[x]['away']
    data_away=file1.loc[file1['Team'] == away].iloc[[0]]
    data_away=data_away.drop(['Team','Match Up','Game Date'],1)
    ######################################### IT FUCKING ENDS HERE ######################################
    data_home=data_home.set_index(data_away.index)
    a=data_home.join(data_away,lsuffix='_left',rsuffix='_right')#doesn't work because indexes don't correspond to one another
    values_to_row=[]
    for i in a.index:
        if a.loc[i,'W/L_left']=='W':
            values_to_row.append(int('0'))#left team won
        else:
            values_to_row.append(int('1'))#right team won
    a['Result']=values_to_row

    values_to_row=[]
    for i in a.index:
        if a.loc[i,'H/A_left']=='home':
            values_to_row.append(int('0'))#left tem is home
        else:
            values_to_row.append(int('1'))#left team is away
    a['Location']=values_to_row

    a=a.drop(['W/L_left','W/L_right','H/A_left','H/A_right'],1)

    ##################################### IMPORTANT ####################################################

    a['Location']=int('0')# NEED TO CORRET THIS BECAUSE MODEL DOESN'T KNOW WHICH TEAM IS HOME (I THINK)

    ##################################### IMPORTANT ####################################################

    # MAYBE INSTEAD OF _LEFT _RIGHT I SHOULD DO _HOME _AWAY
    
    game=a
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers

    a=pd.read_csv('b1.csv')
    a.pop('Unnamed: 0')
    a.pop('Unnamed: 0.1_left')
    a.pop('Unnamed: 0.1_right')

    train_dataset = a.sample(frac=0.8,random_state=666)

    train_stats =train_dataset.describe()
    train_stats.pop('Result')
    train_stats = train_stats.transpose()

    train_labels = train_dataset.pop('Result')

    def norm(x):#maybe this varies from dataset to dataset(47games to all)
        return (x - train_stats['mean']) / train_stats['std']
    game.pop('Result')
    
    # uncomment to get separate games for the support vector machines model
     
    game.to_csv('game_data'+str(x)+'.csv')

    normed_predict=norm(game) #NORM IS NOT WORKING IT WAS BECAUSE THE FILE C:/Users/manuel/Desktop/nbaML/data2.0_WITH_WINRATES.csv    DOESN'T HAVE THE +/- NAMES RIGHT, IT HAS THE NAME AS +/

    model = keras.models.load_model('model_47_51.h5')

    print(home,away,model.predict(normed_predict)[0][0])
    
    pred=model.predict(normed_predict)[0][0]
    if pred<0.5:
        pred=0
    else:
        pred=1
    
    file2=open(path+'/files/my predicts2.csv','a')
    file2.write(home+','+away+','+str(pred)+'\n')
    file2.close()
    
    x=x+1

train_dataset = a.sample(frac=0.7,random_state=666)
test_dataset = a.drop(train_dataset.index)

def norm(x):
    return (x - train_stats['mean']) / train_stats['std']
c=norm(test_dataset)
c.pop('Result')

test_labels = test_dataset.pop('Result')
print(model.evaluate(c,test_labels))
