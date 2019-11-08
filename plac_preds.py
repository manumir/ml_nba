#!/usr/bin/env python3

import time
import datetime
start_time = time.time()

from selenium import webdriver
from bs4 import BeautifulSoup as bs4
import re
import pandas as pd
import functions as f
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

dates,home_odds,away_odds,homes,aways=[],[],[],[],[]
def get_stats():
  driver =webdriver.Chrome(executable_path='C:/Users/dude/Desktop/chromedriver.exe')
  driver.get('https://www.jogossantacasa.pt/web/Placard/eventos?id=22911')
  WebDriverWait(driver,15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.wide-table")))
  
  html=bs4(driver.page_source,'html.parser')
  match=re.search('1X2 INT',str(html))
  if match:
    html=str(html)
    html=html[:match.start()]
    html=bs4(html,'html.parser')
  
  stats=html.find_all("div", class_="content events")
  try:
    stats=bs4((str(stats[0])+str(stats[1])),'html.parser')
  except:
    stats=bs4(str(stats[0]),'html.parser')
  games=stats.find_all("tr")
      
  for tr in games:
    date_div=tr.find_all('td', class_='date')
    dates.append(re.sub(r'\W+','',date_div[0].text).strip("\n"))

    odds_divs=tr.find_all("div", class_="outcome-wrapper")
    
    home=re.sub(r'[^\D]','',odds_divs[0].text)
    home=re.sub(r'\n','',home)
    home=re.sub(r'\xa0','',home)
    home=re.sub(r',','',home)
    homes.append(home)

    away=re.sub(r'[^\D]','',odds_divs[2].text)
    away=re.sub(r'\n','',away)
    away=re.sub(r'\xa0','',away)
    away=re.sub(r',','',away)
    aways.append(away)

    home_odds.append(re.sub(r'[^0-9,]','',odds_divs[0].text).replace(',','.'))
    away_odds.append(re.sub(r'[^0-9,]','',odds_divs[2].text).replace(',','.'))

  driver.quit()

get_stats()

# add the game date
now = datetime.datetime.now()
new_dates=[]
for x in dates:
  new_dates.append(str(now.month)+'/'+str(now.day)+'/'+str(now.year))

real_games=pd.read_csv('games.csv')
df=pd.DataFrame()
df['home']=f.name2acro(homes,'placard')
df['away']=f.name2acro(aways,'placard')
df['date']=new_dates
df['plac_H']=home_odds
df['plac_A']=away_odds
df=df[:len(real_games)]
df=df.sort_values('home')

if len(real_games)>len(df):
  print('\nmissing {} games on plac_log\n'.format(len(real_games)-len(df)))

# delete the '76' on philadelphia odds
for ix in range(len(df)):
  if df.at[ix,'home'] or df.at[ix,'away']=='PHI':
    df.at[ix,'plac_A']=df.at[ix,'plac_A'][-4:]
    df.at[ix,'plac_H']=df.at[ix,'plac_H'][-4:]

curr_path=os.getcwd()
path2logs=curr_path+'\\logs\\'
log=pd.read_csv(path2logs+'plac_log.csv')
log=log.append(df,sort=False)
log.to_csv(path2logs+'plac_log.csv',index=False)