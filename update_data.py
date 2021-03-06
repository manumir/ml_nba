#! /usr/bin/python3

import time
start_time = time.time()

import os
import platform
import sys
from selenium import webdriver
from bs4 import BeautifulSoup as bs4
import pandas as pd
import re
import functions as f
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

os_name=platform.system()
currentpath=os.getcwd()
#os.makedirs(str(os.getcwd())+'\\data\\')

if os_name=='Linux':
	path2data=os.path.join(currentpath,"data/")
else:
	path2data=os.path.join(currentpath,"data\\")

data=pd.read_csv('whole_raw.csv')
last_date=data.at[0,'Game Date']
year='2020'

# 2018 to 2018-2019
def season_name(year):
  if int(year[-2:])+1 < 10:
    add0='0'+str(int(year[-2:])+1)
    return year+'-'+add0
  else:
    return year+'-'+str(int(year[-2:])+1)

def get_stats():
  if os_name=='Linux':
    driver = webdriver.Firefox(executable_path='../geckodriver')
  else:
    driver = webdriver.Chrome(executable_path='C:/Users/dude/Desktop/chromedriver.exe')
  if len(sys.argv)<2:
    driver.get('https://stats.nba.com/teams/boxscores-traditional/?Season='+season_name(year)+'&SeasonType=Regular%20Season')
  else:
    driver.get('https://stats.nba.com/teams/boxscores-traditional/?Season='+season_name(year)+'&SeasonType=Playoffs')
  
  WebDriverWait(driver,25).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.banner-actions-container")))

  path=driver.find_element_by_id("onetrust-accept-btn-handler")
  path.click()
  
  driver.get('https://stats.nba.com/teams/boxscores-traditional/?Season='+season_name(year)+'&SeasonType=Regular%20Season')
	
  WebDriverWait(driver,15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.nba-stat-table__overflow")))

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
      stats=stats[:match.start()-20]
      file.write(stats)  
      print('wrote',i)
      break
    file.write(stats)
    print("wrote",i)

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

if len(sys.argv)<2:
  file=open(path2data+'raw_2019-20.csv','r') # hardcoded cheack notes
  file_existing_lines=file.readlines()
  #file_existing_lines=file_existing_lines[0:1]+file_existing_lines[:0:-1]
  file.close()
  file=open(path2data+'raw_2019-20.csv','w') # hardcoded cheack notes
else:
  file=open(path2data+'raw_2019-20playoffs.csv','r') # hardcoded cheack notes
  file_existing_lines=file.readlines()
  #file_existing_lines=file_existing_lines[0:1]+file_existing_lines[:0:-1]
  file.close()
  file=open(path2data+'raw_2019-20playoffs.csv','w') # hardcoded cheack notes

lines2write=file_existing_lines+lines
for line in lines2write:
  file.write(line)
file.close()

# read data to update
toappend=pd.read_csv(path2data+'raw_2019-20.csv') # hardcoded cheack notes
toappend.pop('Unnamed: 24')
toappend=toappend[-len(lines):]
toappend=toappend.iloc[::-1]

# update whole data.csv
whole_data=pd.read_csv('whole_raw.csv')
whole_data=whole_data.dropna()
whole_data=whole_data.astype('object')
whole_data=whole_data.iloc[::-1]
whole_data=whole_data.append(toappend,sort=False)
whole_data=whole_data.iloc[::-1]
whole_data=whole_data.reset_index(drop=True)
whole_data.to_csv('whole_raw.csv',index=False)

c2_avg=['PTS', 'FGM', 'FGA','FG%', '3PM', '3PA', '3P%',
        'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB',
        'AST', 'TOV', 'STL', 'BLK', 'PF', '+/-']

# get avgs of recent data
toappend=toappend.reset_index(drop=True)
toappend=toappend.astype('object')
for ix in range(len(toappend)):
  print(ix)
  data1=toappend.at[ix,'Game Date']
  team=toappend.at[ix,'Team']
  past=f.get_past_games(whole_data,data1,team,20)
  toappend.at[ix,'winrate 20']=f.create_winrate(past,20)
  toappend.at[ix,'winrate 10']=f.create_winrate(past,10)
  toappend.at[ix,'winrate 5']=f.create_winrate(past,5)
  toappend.at[ix,'fatigue']=f.fatigue(past)
  for c in c2_avg:
    toappend.at[ix,c]=f.get_avgs(past,c)
"""
# update data.csv
data=pd.read_csv('data.csv')
data=data.dropna()
data=data.iloc[::-1]
data=data.append(toappend,sort=False)
data=data.iloc[::-1]
data=data.reset_index(drop=True)
data.to_csv('data.csv',index=False)
"""
# update train.csv
train=pd.read_csv('train.csv')
toappend=f.append2for1(toappend)
toappend['Result']=f.result(toappend)
train=train.iloc[::-1]
train=train.append(toappend,sort=False)
train=train.iloc[::-1]
train.to_csv('train.csv',index=False)
