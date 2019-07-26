#!/usr/bin/python3

#automate the process of predicting games

from selenium import webdriver
from bs4 import BeautifulSoup as bs4

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import re

def get_stats():
    #try:
    driver =webdriver.Chrome(executable_path='C:/Users/dude/Desktop/chromedriver.exe')
    print('program starting')
    driver.get('https://stats.nba.com/schedule/')
    file=open('games.csv','w')#'w')
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "schedule-content__week")))
    html=bs4(driver.page_source,'html.parser')
    
    abc=input('enter today in the format: "February 9"')
    start=re.search(abc,str(html))
    de_f=input('enter tomorrow in the format: "February 9"')
    end=re.search(de_f,str(html))
    
    try:
      html=str(html)[start.start():end.start()]
    except:
      html=str(html)[start.start():len(html)]
    html=bs4(html,'html.parser')
    a=html.find_all("th", class_="schedule-game__team-name")
    a=bs4(str(a),'html.parser')
    
    file.write('away,home\n')
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

'''    except:
        print('something went wrong, colsing...')
        file.close()
        driver.quit()'''

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

file.to_csv('games.csv')


teams=['MEM', 'HOU', 'BKN', 'BOS', 'LAC', 'NOP', 'SAC', 'POR', 'DET', 'UTA', 'CHA', 'SAS', 'WAS', 'TOR','DEN',
       'MIL', 'ATL','GSW', 'DAL', 'ORL', 'PHI', 'NYK', 'LAL', 'CLE', 'OKC', 'MIN', 'CHI', 'MIA', 'PHX', 'IND']

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

file=pd.read_csv('games.csv')
file.pop('Unnamed: 0')
print(file)

# names to acronyms
new_A=[]
for team in file['away'].values:
    x=0
    for name in teams1:
        if name == team:
            name=teams[x]
            new_A.append(name)
        x=x+1
file['away']=new_A

# names to acronyms
new_H=[]
for team in file['home'].values:
    x=0
    for name in teams1:
        if name == team:        
            name=teams[x]
            new_H.append(name)
        x=x+1
file['home']=new_H

print(file)
file.to_csv('games.csv')
