#! /usr/bin/python3

import time
import os
import sys
start_time = time.time()

from selenium import webdriver
from bs4 import BeautifulSoup as bs4
import pandas as pd
import re
import functions as f

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

currentpath=os.getcwd()
#os.makedirs(str(os.getcwd())+'\\data\\')
path2data=os.path.join(currentpath,"data\\")

data=pd.read_csv('data.csv')
last_date=data.at[0,'Game Date']
year=last_date[-4:]

# 2018 to 2018-2019
def season_name(year):
  if int(year[-2:])+1 < 10:
    add0='0'+str(int(year[-2:])+1)
    return year+'-'+add0
  else:
    return year+'-'+str(int(year[-2:])+1)

def get_stats():
    driver = webdriver.Chrome(executable_path='C:/Users/dude/Desktop/chromedriver.exe')
    
    if len(sys.argv)<3:
      driver.get('https://stats.nba.com/teams/boxscores-traditional/?Season='+season_name(year)+'&SeasonType=Regular%20Season')
    else:
      driver.get('https://stats.nba.com/teams/boxscores-traditional/?Season='+season_name(year)+'&SeasonType=Playoffs')
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.nba-stat-table__overflow")))
    try:
      path_2_num_pages=driver.find_element_by_class_name("stats-table-pagination__info")
      NUMBER_OF_PAGES=int(path_2_num_pages.text[-2:])
    except:
      NUMBER_OF_PAGES=1

    file=open(str(path2data)+'data_raw.txt','w')
    i=0
    print(NUMBER_OF_PAGES)
    for i in range(NUMBER_OF_PAGES):
      html=bs4(driver.page_source,'html.parser')
      #features = html.table.thead.tr.text #don't need to scrape this multiple times
      stats=html.table.tbody.text
      match=re.search(last_date,str(stats))
      print(match)
      if match:
        stats=stats[:match.start()-19]
      file.write(stats)

      if NUMBER_OF_PAGES>1:
        path=driver.find_element_by_class_name("stats-table-pagination__next")
        path.click()
      else:
        continue

    file.close()
    driver.quit()

get_stats()
print("scraped in %s seconds" % (time.time() - start_time))

ff=[]
file =open(path2data+'data_raw.txt','r') #,encoding ='cp1252')
file1=file.readlines()

for x in file1:
  x=x.strip('\n')
  x=x.strip(' ')
  x=x + ','

  if x != ',':
    ff.append(x)

file.close()
os.remove(path2data+'data_raw.txt')

file=open(path2data+'data.txt','w')
i=0
for x in ff:
    file.write(x)
    i+=1
    if i==24:
      file.write('\n')
      i=0
file.close()

#try to do this without having to open the file again

filer=open(path2data+'data.txt','r')
lines=filer.readlines()
filer.close()
os.remove(path2data+'data.txt')

if len(sys.argv)<3:
  file=open(path2data+'raw_'+season_name(year)+'.csv','a')
else:
  file=open(path2data+'raw_'+season_name(year)+'playoffs.csv','a')

for line in lines:
  file.write(line)
file.close()

toappend=pd.read_csv(path2data+'raw_'+season_name(year)+'.csv')
toappend.pop('Unnamed: 24')
toappend=toappend[-len(lines):]
toappend=toappend.iloc[::-1]
print(toappend)

data=pd.read_csv('whole_raw_data.csv')
data=data.dropna()
data=data.astype('object')
data=data.iloc[::-1]
data=data.append(toappend,sort=False)
data=data.iloc[::-1]
data=data.reset_index(drop=True)
data.to_csv('whole_raw_data.csv',index=False)
print(data)

c2_avg=['PTS', 'FGM', 'FGA','FG%', '3PM', '3PA', '3P%',
        'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB',
        'AST', 'TOV', 'STL', 'BLK', 'PF', '+/-']

toappend=toappend.reset_index(drop=True)
for ix in range(len(toappend)):
  print(ix)
  data1=toappend.at[ix,'Game Date']
  team=toappend.at[ix,'Team']
  ixs=f.get_past_games(data,data1,team,30)
  past=data.loc[ixs]
  toappend.at[ix,'winrate 30']=f.create_winrate(past,30)
  toappend.at[ix,'winrate 6']=f.create_winrate(past,6)
  
  for c in c2_avg:
    toappend.at[ix,c]=f.get_avgs(past,c)

data=pd.read_csv('data.csv')
data=data.dropna()
data=data.iloc[::-1]
data=data.append(toappend,sort=False)
data=data.iloc[::-1]
data=data.reset_index(drop=True)
print(data)
data.to_csv('data.csv',index=False)

"""
data=pd.read_csv('train.csv')

data=f.append2for1(data)
data['Result']=f.result(data)
data=data.iloc[::-1]
data=data.append(toappend)
data=data.iloc[::-1]
b.to_csv('train.csv',index=False)
"""