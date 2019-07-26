import functions

import pandas as pd

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
  driver =webdriver.Chrome(executable_path=r'C:\Users\dude\Desktop\chromedriver.exe')

  print('program starting')
  driver.get('https://stats.nba.com/teams/boxscores/?Season=ALLTIME&SeasonType=Regular%20Season')
        
  #date='11/20/2018'# in retarded form (us)#2days before today?'11/20/2018'
  datefile=pd.read_csv('b.csv')
  date=str(datefile.at[datefile.index[-1],'Game Date'])
  date=str(datefile.at[0,'Game Date'])
  dia=date[0:3]
  mes=date[3:6]
  year=date[6:len(date)]
  date=str(mes+dia+year)
  print(date)
  #date=input('input last date on data.txt #date from 2 days ago: ')
  file=open('data.txt','w')#'w')
  while True:
    WebDriverWait(driver,500).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.nba-stat-table__overflow")))
    html=bs4(driver.page_source,'html.parser')
    stats= html.table.tbody.text
    match=re.search(date,stats)
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
    f.append('\n')  ###### TAKE _experimenting OFF FOR NORMAL #
  
  if x != ',':
    f.append(x)

file.close()

file=open('data1.txt','w+')
for x in f:
    file.write(x)
file.close()

#try to do this without having to open the file again
filer=open('data1.txt','r')
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

f1=pd.read_csv('data.csv')

#change date format from us to eu
new_dates=[]
old_dates=list(f1['Game Date'].values)
for x in old_dates:
    day=x[3:5]
    month=x[0:2]
    year=x[6:len(x)]
    new_date=day+'/'+month+'/'+year
    new_dates.append(new_date)
f1['Game Date']=new_dates

f=pd.read_csv('finaldata11.csv')
f.pop('Unnamed: 0')

a=f1.append(f,sort=False)

a.to_csv('a.csv')

file=pd.read_csv('data with avgs of 47 games(i think)_with winrates.csv')
file=file.drop(['Unnamed: 0','Unnamed: 0.1'],1)

columns=[]
for column in list(file.columns.values):
    if file[column].dtype!='object':
        columns.append(column)
columns.remove('winrate(69 games)')

list1=list(range(len(columns)))
list2=[]
for x in list1:
    list2.append(x+4)

for i in range(len(f1.index)): 
    date=f1.iloc[[i],2].values[0]
    team=f1.iloc[[i],0].values[0]
    f1.iloc[[i],list2]=functions.get_avgs(functions.create_dataframe(team,date,a),columns)
    f1.at[i,'winrate(69 games)']=functions.create_winrate(team,date,a)
    print(i)

# create a home/away column
values=[]
for value in f1['Match Up'].values:
    if value[4:6]=='vs':
        values.append('home')
    else:
        values.append('away')
f1['H/A']=values

file=pd.read_csv('b.csv')
file=f1.append(file,sort=False)

file.to_csv('b.csv')
