#!/usr/bin/env python3

import time
start_time = time.time()

from selenium import webdriver
from bs4 import BeautifulSoup as bs4

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import re

def get_stats():
    #try:
  driver =webdriver.Chrome(executable_path=r'C:\Users\dude\Desktop\chromedriver.exe')

  print('program starting')
  driver.get('https://stats.nba.com/teams/boxscores/?Season=ALLTIME&SeasonType=Regular%20Season')
        
  date='11/20/2018'# in retarded form (us)#2days before today?'11/20/2018'
                        # date = last date on data.csv
        
  #date=input('input last date on data.txt #date from 2 days ago: ')
  file=open('data.txt','w')#'w')
  while True:
    WebDriverWait(driver,500).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.nba-stat-table__overflow")))
    html=bs4(driver.page_source,'html.parser')
    stats= html.table.tbody.text
    match=re.search(date,stats)
    print(stats)
    if match:
      stats=stats[0:match.start()-16]
      file.write(stats)
      print("found a match and driver is going down boi.")
      driver.quit()
      file.close()
      break
    else:
      file.write(stats)
      path=driver.find_element_by_class_name("stats-table-pagination__next")
      path.click()
#    except:
 #       print('something went wrong')
  #      print("Driver closed.")
   #     file.close()
    #    driver.quit()
            
get_stats()
print("--- %s seconds ---" % (time.time() - start_time))

import os

f=[]
file =open('data.txt','r')                  #,encoding ='cp1252')
file1=file.readlines()

for x in file1:
  x=x.strip('\n')
  x=x + ','
  
  if x == ',':
    f.append('\n')                            ###################### TAKE _experimenting OFF FOR NORMAL ########
  
  if x != ',':
    f.append(x)

file.close()

file=open('data1.txt','w+')
for x in f:
    file.write(x)
file.close()

#try to do this without having to open the file again

filer=open('data1.txt','r')
#filer=open('finaldata1.2.0.txt','r')
lines=filer.readlines()
filer.close()

os.remove("data1.txt")

file=open('data.csv','w')
file.write('Team,Match Up,Game Date,W/L,MIN,PTS,FGM,FGA,FG%,3PM,3PA,3P%,FTM,FTA,FT%,OREB,DREB,REB,AST,STL,BLK,TOV,PF,+/-\n')
for line in lines:
    if line.endswith('\n') and line.index('\n') <30:
        line=line.strip('\n')
        file.write(line)
    else:
        file.write(line[0:len(line)-2]+'\n')
file.close()
print('ended')


import pandas as pd
import numpy as np

file= pd.read_csv('data.csv')

# some cleaning
file[file.columns[7]]=pd.to_numeric(file[file.columns[7]], errors='coerce')
file[file.columns[10]]=pd.to_numeric(file[file.columns[10]], errors='coerce')
file[file.columns[13]]=pd.to_numeric(file[file.columns[13]], errors='coerce')
file=file.dropna(0)

# get team names
teams =[]
for row in file['Team']:
    if row not in teams:
        teams.append(row)
print(teams)
# get columns names
columns=[]
for column in list(file.columns.values):
    if file[column].dtype!='object':
        columns.append(column)

#change date format from us to eu
new_dates=[]
old_dates=list(file['Game Date'].values)
for x in old_dates:
    day=x[3:5]
    month=x[0:2]
    year=x[6:len(x)]
    new_date=day+'/'+month+'/'+year
    new_dates.append(new_date)
file['Game Date']=new_dates

#create a away column
values=[]
for value in file['Match Up'].values:
    if value[4:6]=='vs':
        values.append('home')
    else:
        values.append('away')
#print(values)
file['H/A']=values

#create a function to determine if a date is sooner than another date
def datecomp(date1,date2):
    if date1[6:len(date1)]>date2[6:len(date2)]:
        #print("date1's year is greater than date2's year")
        return date2
    if date1[6:len(date1)]<date2[6:len(date2)]:
        #print("date2's year is greater than date1's year")
        return date1
    
    if date1[6:len(date1)]==date2[6:len(date2)]:
        if date1[3:5]>date2[3:5]:
            #print("date1's month is greater than date2's month")
            return date2
    if date1[6:len(date1)]==date2[6:len(date2)]:
        if date1[3:5]<date2[3:5]:
            #print("date2's month is greater than date1's month")
            return date1
        
    if date1[6:len(date1)]==date2[6:len(date2)]:
        if date1[3:5]==date2[3:5]:
            if date1[0:2]>date2[0:2]:
                #print("date1's day is greater than date2's day")
                return date2
    if date1[6:len(date1)]==date2[6:len(date2)]:
        if date1[3:5]==date2[3:5]:
            if date1[0:2]<date2[0:2]:
                #print("date2's day is greater than date1's day")
                return date1
            
    if date1[6:len(date1)]==date2[6:len(date2)]:
        if date1[3:5]==date2[3:5]:
            if date1[0:2]==date2[0:2]:
                return 0

# create a data frame of games before a certain date
def create_dataframe (team,date):
    rows=file.loc[file['Team'] == team]
    dates=[]
    for value in rows['Game Date'].values:
        if datecomp(value,date)==value:
            dates.append(rows.loc[rows['Game Date']==value])
    if dates == []:
        return 0
    else:
        data=dates[0]
        data=data.append(dates[0:len(dates)]) #REPEATING A ROW/ RUN TO RESOLVE
        return data.drop(data.index[0])

# get averages for each team        
def get_avgs(dataframe):
    try:
        dataframe=dataframe.iloc[list(range(15))]
        avgs=[]
        for column in columns:
            divider=0
            count=0
            for x in dataframe[column]:
                count=count + int(x)
                divider=divider+1
            avg=float(count/divider)
            avgs.append(avg)
        return avgs
    except:
        return 0

list1=list(range(len(columns)))
list2=[]
for x in list1:
    list2.append(x+4)
#print(file)
'''EVENTUALLY SOME DATES IS GOING TO BE EMPTY'''

for i in range(len(file.index)):
    date=file.iloc[[i],2].values[0]
    team=file.iloc[[i],0].values[0]
    if get_avgs(create_dataframe(team,date)) != 0:
        file.iloc[[i],list2]=get_avgs(create_dataframe(team,date))
    print(i)
    
print(file)
file.to_csv('data_with_avgs1.csv')

print('program ended')


file= pd.read_csv('data_with_avgs1.csv')
file.pop('Unnamed: 0')

# get team names
teams =[]
for row in file['Team']:
    if row not in teams:
        teams.append(row)

# get columns names
columns=[]
for column in list(file.columns.values):
    if file[column].dtype!='object':
        columns.append(column)
            
def create_winrate(team,date):
    rows=file.loc[file['Team'] == team]
    dates=[]
    for value in rows['Game Date'].values:
        if datecomp(value,date)==value:
            dates.append(rows.loc[rows['Game Date']==value])
    if dates == []:
        return 0
    else:
        data=dates[0]
        data=data.append(dates[0:len(dates)])#REPEATING A ROW/ RUN TO RESOLVE
        data =data.drop(data.index[0])
        try:
            data=data.iloc[list(range(15))]
            b=0
            for x in data['W/L'].values:
                if x == 'W':
                    b=b+1
            return float(b/len(data))*100
        except:
            return int('50')#bandage to fix last 69 games of file

#print(file[0:4]['Team'])
#print(create_winrate('WAS',file.iloc[0]['Game Date']))

values_to_add=[]
for i in range(len(file.index)):
    date=file.iloc[i]['Game Date']
    team=file.iloc[i]['Team']
    values_to_add.append(create_winrate(team,date))
    #file.iloc[i]['winrate(69 games)']=create_winrate(team,date)
    print(i)
    

file['winrate(69 games)']=values_to_add
print(file['winrate(69 games)'].values)
file.to_csv('data_with_avgs1_WITH_WINRATES.csv')


file=pd.read_csv('avgs_47_games_WITH_WINRATES.csv')
file.pop('Unnamed: 0')
file.pop('Unnamed: 0.1')
file.pop('winrate(69 games)')
file.pop('MIN')

columns=[]
for column in list(file.columns.values):
    if file[column].dtype!='object':
        columns.append(column)
columns.append('winrate(69 games)')

other_columns=[]
for column in list(file.columns.values):
    if file[column].dtype=='object':
        other_columns.append(column)

other_columns_index=list(range(len(other_columns)))

def get_avgs(dataframe):
    try:
        avgs=[]
        for column in columns:
            divider=0
            count=0
            for x in dataframe[column]:
                count=count + int(x)
                divider=divider+1
            avg=float(count/divider)
            avgs.append(avg)
        return avgs
    except:
        print('something went wrong dude')
        
file=pd.read_csv('avgs_47_games_WITH_WINRATES.csv')
file.pop('Unnamed: 0')
file.pop('Unnamed: 0.1')
file.pop('MIN')

file1=pd.read_csv('data_with_avgs1_WITH_WINRATES.csv')
file1.pop('Unnamed: 0')
file1.pop('MIN')

#clean file
import os 
path=os.getcwd()
file2=open(path+'/files/my predicts.csv','w')
file2.write('Home,Away,predicts\n')
file2.close()

auto=pd.read_csv('games.csv')

x=0
while x < len(auto.index):
####################################### NEED TO GET RID OF THIS SPAGETHI CODE #######################
    home=auto.iloc[x]['home team']

    file00=file1.loc[file1['Team'] ==home].iloc[[0]]
    file11=file.loc[file['Team'] ==home].iloc[[0]]
    file0=pd.concat([file00,file11])

    f1=pd.DataFrame(data=get_avgs(file0),index=columns).transpose()
    f=pd.DataFrame(columns=other_columns,data=file0[other_columns].iloc[[0]])
    df=f.join(f1)
    df[columns]=f1[columns].values[0]

    away=auto.iloc[x]['away team']

    file00=file1.loc[file1['Team'] == away].iloc[[0]]
    file11=file.loc[file['Team'] == away].iloc[[0]]
    file0=pd.concat([file00,file11])

    f1=pd.DataFrame(data=get_avgs(file0),index=columns).transpose()
    f=pd.DataFrame(columns=other_columns,data=file0[other_columns].iloc[[0]])
    df2=f.join(f1)
    df2[columns]=f1[columns].values[0]
    ######################################### IT FUCKING ENDS HERE ###############################################################

    df=df.set_index(df2.index)
    a=df.join(df2,lsuffix='_left',rsuffix='_right')#doesn't work because indexes don't correspond to one another

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
    a=a.drop(['Team_left','Team_right','Match Up_left','Game Date_left','Match Up_right','Game Date_right'],1)

    ##################################### IMPORTANT ####################################################

    a['Location']=int('0')# NEED TO CORRET THIS BECAUSE MODEL DOESN'T KNOW WHICH TEAM IS HOME (I THINK)

    ##################################### IMPORTANT ####################################################

    # MAYBE INSTEAD OF _LEFT _RIGHT I SHOULD DO _HOME _AWAY

    a.to_csv('data2.0_WITH_WINRATES.csv')
    b=a

    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers

    a=pd.read_csv('data2.0_WITH_WINRATES1.csv')
    a=a.drop('Unnamed: 0',1)

    train_dataset = a.sample(frac=0.8,random_state=666)

    train_stats =train_dataset.describe()
    train_stats.pop('Result')
    train_stats = train_stats.transpose()

    train_labels = train_dataset.pop('Result')

    def norm(x):#maybe this varies from dataset to dataset(47games to all)
        return (x - train_stats['mean']) / train_stats['std']
    b.pop('Result')

    normed_predict=norm(b) #NORM IS NOT WORKING IT WAS BECAUSE THE FILE C:/Users/manuel/Desktop/nbaML/data2.0_WITH_WINRATES.csv
                           #DOESN'T HAVE THE +/- NAMES RIGHT, IT HAS THE NAME AS +/


    model = keras.models.load_model('model_47_games.h5')

    print(home,away,model.predict(normed_predict)[0][0])
    
    pred=model.predict(normed_predict)[0][0]
    if pred<=0.5:
        pred=0
    else:
        pred=1
    
    file2=open(path+'/files/my predicts.csv','a')

    file2.write(home+','+away+','+str(pred)+'\n')

    file2.close()

    x=x+1
    
print('\ndone')
## have a feeeling this is getting the wrong data to predict from
## maybe a should be able to verify the input
## e.g check if winrates match (input and real life)
## jeez my english/expression is bad


file=pd.read_csv(path+'/files/my predicts.csv')
file=file.sort_values(by='Home')
file.to_csv(path+'/files/my predicts.csv')


train_dataset = a.sample(frac=0.7,random_state=666)
test_dataset = a.drop(train_dataset.index)

def norm(x):
    return (x - train_stats['mean']) / train_stats['std']
c=norm(test_dataset)
c.pop('Result')

test_labels = test_dataset.pop('Result')
print(model.evaluate(c,test_labels))


import time
start_time = time.time()

from selenium import webdriver
from bs4 import BeautifulSoup as bs4

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import re

def get_stats():
    #try:
  driver =webdriver.Chrome(executable_path=r'C:\Users\dude\Desktop\chromedriver.exe')

  print('program starting')
  driver.get('https://stats.nba.com/teams/boxscores/?Season=ALLTIME&SeasonType=Regular%20Season')
        
  date='11/20/2018'# in retarded form (us)#2days before today?'11/20/2018'
                        # date = last date on data.csv
        
  #date=input('input last date on data.txt #date from 2 days ago: ')
  file=open('data.txt','w')#'w')
  while True:
    WebDriverWait(driver,500).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.nba-stat-table__overflow")))
    html=bs4(driver.page_source,'html.parser')
    stats= html.table.tbody.text
    match=re.search(date,stats)
    print(stats)
    if match:
      stats=stats[0:match.start()-16]
      file.write(stats)
      print("found a match and driver is going down boi.")
      driver.quit()
      file.close()
      break
    else:
      file.write(stats)
      path=driver.find_element_by_class_name("stats-table-pagination__next")
      path.click()
#    except:
 #       print('something went wrong')
  #      print("Driver closed.")
   #     file.close()
    #    driver.quit()
            
get_stats()
print("--- %s seconds ---" % (time.time() - start_time))

import os

f=[]
file =open('data.txt','r')                  #,encoding ='cp1252')
file1=file.readlines()

for x in file1:
  x=x.strip('\n')
  x=x + ','
  
  if x == ',':
    f.append('\n')                            ###################### TAKE _experimenting OFF FOR NORMAL ########
  
  if x != ',':
    f.append(x)

file.close()

file=open('data1.txt','w+')
for x in f:
    file.write(x)
file.close()

#try to do this without having to open the file again

filer=open('data1.txt','r')
#filer=open('finaldata1.2.0.txt','r')
lines=filer.readlines()
filer.close()

os.remove("data1.txt")

file=open('data.csv','w')
file.write('Team,Match Up,Game Date,W/L,MIN,PTS,FGM,FGA,FG%,3PM,3PA,3P%,FTM,FTA,FT%,OREB,DREB,REB,AST,STL,BLK,TOV,PF,+/-\n')
for line in lines:
    if line.endswith('\n') and line.index('\n') <30:
        line=line.strip('\n')
        file.write(line)
    else:
        file.write(line[0:len(line)-2]+'\n')
file.close()
print('ended')


import pandas as pd
import numpy as np

file= pd.read_csv('data.csv')

# some cleaning
file[file.columns[7]]=pd.to_numeric(file[file.columns[7]], errors='coerce')
file[file.columns[10]]=pd.to_numeric(file[file.columns[10]], errors='coerce')
file[file.columns[13]]=pd.to_numeric(file[file.columns[13]], errors='coerce')
file=file.dropna(0)

# get team names
teams =[]
for row in file['Team']:
    if row not in teams:
        teams.append(row)
print(teams)
# get columns names
columns=[]
for column in list(file.columns.values):
    if file[column].dtype!='object':
        columns.append(column)

#change date format from us to eu
new_dates=[]
old_dates=list(file['Game Date'].values)
for x in old_dates:
    day=x[3:5]
    month=x[0:2]
    year=x[6:len(x)]
    new_date=day+'/'+month+'/'+year
    new_dates.append(new_date)
file['Game Date']=new_dates

#create a away column
values=[]
for value in file['Match Up'].values:
    if value[4:6]=='vs':
        values.append('home')
    else:
        values.append('away')
#print(values)
file['H/A']=values

#create a function to determine if a date is sooner than another date
def datecomp(date1,date2):
    if date1[6:len(date1)]>date2[6:len(date2)]:
        #print("date1's year is greater than date2's year")
        return date2
    if date1[6:len(date1)]<date2[6:len(date2)]:
        #print("date2's year is greater than date1's year")
        return date1
    
    if date1[6:len(date1)]==date2[6:len(date2)]:
        if date1[3:5]>date2[3:5]:
            #print("date1's month is greater than date2's month")
            return date2
    if date1[6:len(date1)]==date2[6:len(date2)]:
        if date1[3:5]<date2[3:5]:
            #print("date2's month is greater than date1's month")
            return date1
        
    if date1[6:len(date1)]==date2[6:len(date2)]:
        if date1[3:5]==date2[3:5]:
            if date1[0:2]>date2[0:2]:
                #print("date1's day is greater than date2's day")
                return date2
    if date1[6:len(date1)]==date2[6:len(date2)]:
        if date1[3:5]==date2[3:5]:
            if date1[0:2]<date2[0:2]:
                #print("date2's day is greater than date1's day")
                return date1
            
    if date1[6:len(date1)]==date2[6:len(date2)]:
        if date1[3:5]==date2[3:5]:
            if date1[0:2]==date2[0:2]:
                return 0

# create a data frame of games before a certain date
def create_dataframe (team,date):
    rows=file.loc[file['Team'] == team]
    dates=[]
    for value in rows['Game Date'].values:
        if datecomp(value,date)==value:
            dates.append(rows.loc[rows['Game Date']==value])
    if dates == []:
        return 0
    else:
        data=dates[0]
        data=data.append(dates[0:len(dates)]) #REPEATING A ROW/ RUN TO RESOLVE
        return data.drop(data.index[0])

# get averages for each team        
def get_avgs(dataframe):
    try:
        dataframe=dataframe.iloc[list(range(15))]
        avgs=[]
        for column in columns:
            divider=0
            count=0
            for x in dataframe[column]:
                count=count + int(x)
                divider=divider+1
            avg=float(count/divider)
            avgs.append(avg)
        return avgs
    except:
        return 0

list1=list(range(len(columns)))
list2=[]
for x in list1:
    list2.append(x+4)
#print(file)
'''EVENTUALLY SOME DATES IS GOING TO BE EMPTY'''

for i in range(len(file.index)):
    date=file.iloc[[i],2].values[0]
    team=file.iloc[[i],0].values[0]
    if get_avgs(create_dataframe(team,date)) != 0:
        file.iloc[[i],list2]=get_avgs(create_dataframe(team,date))
    print(i)
    
print(file)
file.to_csv('data_with_avgs1.csv')

print('program ended')


file= pd.read_csv('data_with_avgs1.csv')
file.pop('Unnamed: 0')

# get team names
teams =[]
for row in file['Team']:
    if row not in teams:
        teams.append(row)

# get columns names
columns=[]
for column in list(file.columns.values):
    if file[column].dtype!='object':
        columns.append(column)
            
def create_winrate(team,date):
    rows=file.loc[file['Team'] == team]
    dates=[]
    for value in rows['Game Date'].values:
        if datecomp(value,date)==value:
            dates.append(rows.loc[rows['Game Date']==value])
    if dates == []:
        return 0
    else:
        data=dates[0]
        data=data.append(dates[0:len(dates)])#REPEATING A ROW/ RUN TO RESOLVE
        data =data.drop(data.index[0])
        try:
            data=data.iloc[list(range(15))]
            b=0
            for x in data['W/L'].values:
                if x == 'W':
                    b=b+1
            return float(b/len(data))*100
        except:
            return int('50')#bandage to fix last 69 games of file

#print(file[0:4]['Team'])
#print(create_winrate('WAS',file.iloc[0]['Game Date']))

values_to_add=[]

for i in range(len(file.index)):
    date=file.iloc[i]['Game Date']
    team=file.iloc[i]['Team']
    values_to_add.append(create_winrate(team,date))
    #file.iloc[i]['winrate(69 games)']=create_winrate(team,date)
    print(i)
    

file['winrate(69 games)']=values_to_add
print(file['winrate(69 games)'].values)
file.to_csv('data_with_avgs1_WITH_WINRATES.csv')


file=pd.read_csv('avgs_47_games_WITH_WINRATES.csv')
file.pop('Unnamed: 0')
file.pop('Unnamed: 0.1')
file.pop('winrate(69 games)')
file.pop('MIN')

columns=[]
for column in list(file.columns.values):
    if file[column].dtype!='object':
        columns.append(column)
columns.append('winrate(69 games)')

other_columns=[]
for column in list(file.columns.values):
    if file[column].dtype=='object':
        other_columns.append(column)

other_columns_index=list(range(len(other_columns)))

def get_avgs(dataframe):
    try:
        avgs=[]
        for column in columns:
            divider=0
            count=0
            for x in dataframe[column]:
                count=count + int(x)
                divider=divider+1
            avg=float(count/divider)
            avgs.append(avg)
        return avgs
    except:
        print('something went wrong dude')
        
file=pd.read_csv('avgs_47_games_WITH_WINRATES.csv')
file.pop('Unnamed: 0')
file.pop('Unnamed: 0.1')
file.pop('MIN')

file1=pd.read_csv('data_with_avgs1_WITH_WINRATES.csv')
file1.pop('Unnamed: 0')
file1.pop('MIN')

#clean file
#file2=open('C:/Users/manuel/Desktop/MODEL WORKS/model evaluater/my predicts.csv','w')

import os 
path=os.getcwd()
file2=open(path+'/files/my predicts.csv','w')
file2.write('Home,Away,predicts\n')
file2.close()

auto=pd.read_csv('games.csv')

x=0
while x < len(auto.index):
    ####################################### NEED TO GET RID OF THIS SPAGETHI CODE #################################################
    home=auto.iloc[x]['home team']

    file00=file1.loc[file1['Team'] ==home].iloc[[0]]
    file11=file.loc[file['Team'] ==home].iloc[[0]]
    file0=pd.concat([file00,file11])

    f1=pd.DataFrame(data=get_avgs(file0),index=columns).transpose()
    f=pd.DataFrame(columns=other_columns,data=file0[other_columns].iloc[[0]])
    df=f.join(f1)
    df[columns]=f1[columns].values[0]

    away=auto.iloc[x]['away team']

    file00=file1.loc[file1['Team'] == away].iloc[[0]]
    file11=file.loc[file['Team'] == away].iloc[[0]]
    file0=pd.concat([file00,file11])

    f1=pd.DataFrame(data=get_avgs(file0),index=columns).transpose()
    f=pd.DataFrame(columns=other_columns,data=file0[other_columns].iloc[[0]])
    df2=f.join(f1)
    df2[columns]=f1[columns].values[0]
    ######################################### IT FUCKING ENDS HERE ###############################################################

    df=df.set_index(df2.index)
    a=df.join(df2,lsuffix='_left',rsuffix='_right')#doesn't work because indexes don't correspond to one another

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
    a=a.drop(['Team_left','Team_right','Match Up_left','Game Date_left','Match Up_right','Game Date_right'],1)

    ##################################### IMPORTANT ####################################################

    a['Location']=int('0')# NEED TO CORRET THIS BECAUSE MODEL DOESN'T KNOW WHICH TEAM IS HOME (I THINK)

    ##################################### IMPORTANT ####################################################

    # MAYBE INSTEAD OF _LEFT _RIGHT I SHOULD DO _HOME _AWAY

    a.to_csv('data2.0_WITH_WINRATES.csv')
    b=a

    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers

    a=pd.read_csv('data2.0_WITH_WINRATES1.csv')
    a=a.drop('Unnamed: 0',1)

    train_dataset = a.sample(frac=0.8,random_state=666)

    train_stats =train_dataset.describe()
    train_stats.pop('Result')
    train_stats = train_stats.transpose()

    train_labels = train_dataset.pop('Result')

    def norm(x):#maybe this varies from dataset to dataset(47games to all)
        return (x - train_stats['mean']) / train_stats['std']
    b.pop('Result')

    normed_predict=norm(b) #NORM IS NOT WORKING IT WAS BECAUSE THE FILE C:/Users/manuel/Desktop/nbaML/data2.0_WITH_WINRATES.csv
                           #DOESN'T HAVE THE +/- NAMES RIGHT, IT HAS THE NAME AS +/


    model = keras.models.load_model('model_47_games.h5')

    print(home,away,model.predict(normed_predict)[0][0])
    
    pred=model.predict(normed_predict)[0][0]
    if pred<=0.5:
        pred=0
    else:
        pred=1
    
    file2=open(path+'/files/my predicts.csv','a')

    file2.write(home+','+away+','+str(pred)+'\n')

    file2.close()

    x=x+1
    
print('\ndone')
## have a feeeling this is getting the wrong data to predict from
## maybe a should be able to verify the input
## e.g check if winrates match (input and real life)
## jeez my english/expression is bad


file=pd.read_csv(path+'/files/my predicts.csv')
file=file.sort_values(by='Home')
file.to_csv(path+'/files/my predicts.csv')


train_dataset = a.sample(frac=0.7,random_state=666)
test_dataset = a.drop(train_dataset.index)

def norm(x):
    return (x - train_stats['mean']) / train_stats['std']
c=norm(test_dataset)
c.pop('Result')

test_labels = test_dataset.pop('Result')
print(model.evaluate(c,test_labels))

