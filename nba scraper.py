#! /usr/bin/python3

# usage:

# scrape nba season 2008-2009:
# nba scraper.py 2008

# scrape nba playoffs 2008-2009:
# nba scraper.py 2008 'anything here'

import time
import os
import sys
start_time = time.time()

from selenium import webdriver
from bs4 import BeautifulSoup as bs4

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

year=str(sys.argv[1])

currentpath=os.getcwd()
#os.makedirs(str(os.getcwd())+'\\data\\')
path2data=os.path.join(currentpath,"data\\")

# 2019 to 19-20
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

f=[]
file =open(path2data+'data_raw.txt','r') #,encoding ='cp1252')
file1=file.readlines()

for x in file1:
  x=x.strip('\n')
  x=x.strip(' ')
  x=x + ','

  if x != ',':
    f.append(x)

file.close()
os.remove(path2data+'data_raw.txt')

file=open(path2data+'data.txt','w')
i=0
for x in f:
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
  file=open(path2data+'raw_'+season_name(year)+'.csv','w')
else:
  file=open(path2data+'raw_'+season_name(year)+'playoffs.csv','w')

file.write('Team,Match Up,Game Date,W/L,MIN,PTS,FGM,FGA,FG%,3PM,3PA,3P%,FTM,FTA,FT%,OREB,DREB,REB,AST,TOV,STL,BLK,PF,+/-,\n')
for line in lines:
  file.write(line)
file.close()

