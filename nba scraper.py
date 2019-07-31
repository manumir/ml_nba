#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
start_time = time.time()

from selenium import webdriver
from bs4 import BeautifulSoup as bs4

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

#from selenium.webdriver.firefox.options import Options

def get_stats():

    print('program starting')
    #options = Options()
    #options.add_argument("--headless")
    #firefox_options=options,
    driver = webdriver.Firefox(executable_path=r'C:\Users\manuel\Desktop\a\web drivers\geckodriver-v0.23.0-win64\geckodriver.exe')
    print('driver is initalized')

    driver.get('https://stats.nba.com/teams/boxscores/?Season=ALLTIME&SeasonType=Regular%20Season')
    print("Firefox Headless Browser Invoked")

    file=open('data1.txt','w+')
    while True:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.nba-stat-table__overflow")))

        html=bs4(driver.page_source,'html.parser')
        #features = html.table.thead.tr.text #don't need to scrape this multiple times
        stats= html.table.tbody.text 

        file.write(stats)

        path=driver.find_element_by_class_name("stats-table-pagination__next")
        path.click()

        print("Driver closed.")
        file.close()
        driver.quit()
        
get_stats()
print("--- %s seconds ---" % (time.time() - start_time))

