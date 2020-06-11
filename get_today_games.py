 #!/usr/bin/python3

#automate the process of predicting games
import datetime
import platform 
from selenium import webdriver
from bs4 import BeautifulSoup as bs4

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import re

def get_stats():
    if platform.system()=='Linux':
      driver = webdriver.Firefox(executable_path='../geckodriver')
    else:
      driver = webdriver.Chrome(executable_path='C:/Users/dude/Desktop/chromedriver.exe')
    print('program starting')
    driver.get('https://stats.nba.com/schedule/')
    file=open('games.csv','w')#'w')
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "schedule-content__week")))
    #driver.execute_script("window.scrollTo(0,0)")
    #hide_prev_games=driver.find_element_by_class_name("switch-paddle")
    #hide_prev_games.click()
    html=bs4(driver.page_source,'html.parser')

    # eliminate zeros on the left of today 
    today=datetime.date.today()
    today=today.strftime("%B %d")
    day=str(today[-2:])
    today=str(today)[:-2]+str(int(day))
    start=re.search(today,str(html))

    # eliminate zeros on the left of tomorrow
    tomorrow=(datetime.date.today() + datetime.timedelta(days=1)).strftime("%B %d")
    day=str(tomorrow[-2:])
    tomorrow=str(tomorrow)[:-2]+str(int(day))
    end=re.search(tomorrow,str(html))
    if end == None:
        tomorrow=(datetime.date.today() + datetime.timedelta(days=2)).strftime("%B %d")
        day=str(tomorrow[-2:])
        tomorrow=str(tomorrow)[:-2]+str(int(day))
        end=re.search(tomorrow,str(html))
    try:
        html=str(html)[start.start():end.start()]
    except:
        html=str(html)[start.start():]
    html=bs4(html,'html.parser')
    a=html.find_all("th", class_="schedule-game__team-name")
    a=bs4(str(a),'html.parser')
    
    file.write('away,home,date\n')
    file.write(' ')## to make all names the same
    
    for x in a.text:
        if x != '\n' and x != ', \n' and x != '[' and x != ']':
            x=x.strip('\n')
            file.write(x)
            if x ==',':
                file.write('\n')

    file.close()
    print('finished')
    driver.quit()
get_stats()

import pandas as pd

file=pd.read_csv('games.csv')

# remove the space in the start of name
new_names=[]
for x in file['away'].values:
    new_names.append(x[1:len(x)])
file['away']=new_names

# merge away team and home team to same line
home=[]
for i in range(len(file)):
    if i %2 ==1:
        home.append(file.loc[i]['away'])
        file=file.drop(i)
file['home']=home

file.to_csv('games.csv',index=False)

teams=['MEM', 'HOU', 'BKN', 'BOS', 'LAC', 'NOP', 'SAC', 'POR', 'DET', 'UTA', 'CHA', 'SAS', 'WAS', 'TOR','DEN','MIL', 'ATL','GSW', 'DAL', 'ORL', 'PHI', 'NYK', 'LAL', 'CLE', 'OKC', 'MIN', 'CHI', 'MIA', 'PHX', 'IND']

teams1=['Boston Celtics','Brooklyn Nets','New York Knicks','Philadelphia 76ers','Toronto Raptors',
'Chicago Bulls','Cleveland Cavaliers','Detroit Pistons','Indiana Pacers','Milwaukee Bucks',
'Atlanta Hawks','Charlotte Hornets','Miami Heat','Orlando Magic','Washington Wizards',
'Dallas Mavericks','Houston Rockets','Memphis Grizzlies','New Orleans Pelicans','San Antonio Spurs',
'Denver Nuggets','Minnesota Timberwolves','Oklahoma City Thunder','Portland Trail Blazers','Utah Jazz',
'Golden State Warriors','LA Clippers','Los Angeles Lakers','Phoenix Suns','Sacramento Kings']

# sort teams names and teams acronyms
teams.sort()
teams1.sort()

# bos and bkn are switched
x=teams[1]
teams[1]=teams[2]
teams[2]=x

#sas and sac are switched
#x=teams[25]
#teams[25]=teams[26]
#teams[26]=x

# por and tor are switched
teams1.pop(24)
#teams1.pop(27)
teams1.insert(24,'Portland Trail Blazers')

# names to acronyms
file=pd.read_csv('games.csv')
new_H=[]
for team in file['home'].values:
    x=0
    for name in teams1:
        if name == team:        
            name=teams[x]
            new_H.append(name)
        x=x+1
file['home']=new_H

new_A=[]
for team in file['away'].values:
    x=0
    for name in teams1:
        if name == team:
            name=teams[x]
            new_A.append(name)
        x=x+1
file['away']=new_A


today=datetime.date.today()
today=today.strftime("%m/%d/%Y")
date=[]
for x in range(len(file)):
    date.append(today)
file['date']=date

file=file.sort_values('home')
file.to_csv('games.csv',index=False)
