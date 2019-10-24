#!/usr/bin/env python3

import time
start_time = time.time()

from selenium import webdriver
from bs4 import BeautifulSoup as bs4
import re
import pandas as pd
import functions as f

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

dates,home_odds,away_odds,homes,aways=[],[],[],[],[]
def get_stats():
  driver =webdriver.Chrome(executable_path='C:/Users/dude/Desktop/chromedriver.exe')
    
  driver.get('https://www.jogossantacasa.pt/web/Placard/eventos?id=22911')

  WebDriverWait(driver,15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.wide-table")))
  html=bs4(driver.page_source,'html.parser')
  """

    match=re.search('1X2 INT',str(html))
    if match:
      html=html[0:match.start()-1]
      html=bs4(html,'html.parser')
  """

  stats=html.find_all("div", class_="content events")
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

df=pd.DataFrame()
df['away']=f.name2acro(aways,'placard')
df['home']=f.name2acro(homes,'placard')
df['date']=dates
df['plac_home']=home_odds
df['plac_away']=away_odds

log=pd.read_csv('log.csv')
log=log.append(df)
log.to_csv('log.csv',index=False)