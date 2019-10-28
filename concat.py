import pandas as pd
import glob
import os

curr_path=os.getcwd()
path2files=curr_path+'\\data\\'
files=glob.glob(path2files+'*.csv')

whole_data=pd.DataFrame(columns=['Team','Match Up','Game Date','W/L','MIN','PTS','FGM','FGA','FG%','3PM',
				'3PA','3P%','FTM','FTA','FT%','OREB','DREB','REB','AST','TOV','STL','BLK','PF','+/-'])

lines=[]
for name in files:
  print(name)
  file=pd.read_csv(name)
  file=file.iloc[::-1]
  whole_data=whole_data.append(file,sort=False)

whole_data.pop('Unnamed: 24')
whole_data=whole_data[::-1]
whole_data.to_csv('whole_raw.csv',index=False)
