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
import platform

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

os_name=platform.system()

if os_name=='Linux':
	driver = webdriver.Firefox(executable_path='../geckodriver')
else:
	driver = webdriver.Chrome(executable_path='C:/Users/dude/Desktop/chromedriver.exe')
driver.get('https://placard.jogossantacasa.pt/PlacardWeb/Events?CompetionName=NBA&RegionName=E.U.A.&SelectedCompetitionId=23164&SelectedDate='+input('year(2020)-month(08)-day(04): ')+'&SelectedModalityId=basketball')

WebDriverWait(driver,15).until(EC.presence_of_element_located((By.ID, "b5-l4-0-b8-ContentWrapper")))

html=bs4(driver.page_source,'html.parser')

# teams field
teams=html.find_all("span", class_="font-size20")

# odds field
odds=html.find_all("span", class_="odd ThemeGrid_MarginGutter")

driver.quit()

# start preprocessing
real_games=pd.read_csv('games.csv')

# get only nba teams
teams=teams[:len(real_games)*2]
home , away = [],[]
i=0
while i < len(teams):
	if i % 2 == 0:
		home.append(str(teams[i].text))
	else:
		away.append(str(teams[i].text))
	i=i+1

# get home and away odds
home_odds , away_odds=[],[]
odds=odds[-len(home) * 3:]
i=0
while i < len(odds):
	odd=str(odds[i].text).replace(',','.')
	home_odds.append(float(odd))
	i=i+3
i=2
while i < len(odds):
	odd=str(odds[i].text).replace(',','.')
	away_odds.append(float(odd))
	i=i+3

df=pd.DataFrame()
df['home']=f.name2acro(home,'placard')
df['away']=f.name2acro(away,'placard')
df['date']=real_games['date']
df['plac_H']=home_odds
df['plac_A']=away_odds

df=df.sort_values('home')
print(df)

if len(real_games)>len(df):
  print('\nmissing {} games on plac_log\n'.format(len(real_games)-len(df)))
  #sys.quit()

"""
# delete the '76' on philadelphia odds
for ix in range(len(df)):
  if df.at[ix,'home'] or df.at[ix,'away']=='PHI':
    df.at[ix,'plac_A']=df.at[ix,'plac_A'][-4:]
    df.at[ix,'plac_H']=df.at[ix,'plac_H'][-4:]
"""

curr_path=os.getcwd()
if os_name=='Linux':
	path2logs=curr_path+'/logs/'
else:
	path2logs=curr_path+'\\logs\\'

log=pd.read_csv(path2logs+'plac_log.csv')
log=log.append(df,sort=False)
log.to_csv(path2logs+'plac_log.csv',index=False)

