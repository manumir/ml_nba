import pandas as pd
import glob
import os

curr_path=os.getcwd()
path2files=curr_path+'\\data\\'
files=glob.glob(path2files+'*.csv')

lines=['Team,Match Up,Game Date,W/L,MIN,PTS,FGM,FGA,FG%,3PM,3PA,3P%,FTM,FTA,FT%,OREB,DREB,REB,AST,TOV,STL,BLK,PF,+/-,\n']

for name in files:
  print(name)
  file=open(name,'r')
  lines+=file.readlines()
  file.close()

file=open('whole_data_raw.csv','w')
for line in lines:
  file.write(line)
file.close()

