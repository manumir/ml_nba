import functions
import pandas as pd
import time
start_time = time.time()

from selenium import webdriver
from bs4 import BeautifulSoup as bs4

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import re

def get_stats():
  driver =webdriver.Chrome(executable_path=r'C:\Users\dude\Desktop\chromedriver.exe')

  print('program starting')
  driver.get('https://stats.nba.com/teams/boxscores/?Season=ALLTIME&SeasonType=Playoffs')
        
  file=open('data_playoffs.txt','w')
  while True:
    try:
      WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.nba-stat-table__overflow")))
      html=bs4(driver.page_source,'html.parser')
      stats= html.table.tbody.text
      file.write(stats)
      path=driver.find_element_by_class_name("stats-table-pagination__next")
      path.click()
    except:
      break

get_stats()
print("--- %s seconds ---" % (time.time() - start_time))
