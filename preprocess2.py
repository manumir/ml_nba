import pandas as pd

data=pd.read_csv('train.csv')

a=data.loc[[0]]
ix=0
while ix < len(data):
  if ix != 0:
    a=a.append(data.loc[[ix]])
  ix+=2

b=data.loc[[1]]
ix=1
while ix < len(data):
  if ix != 1:
    b=b.append(data.loc[[ix]])
  ix+=2

a=a.reset_index(drop=True)
b=b.reset_index(drop=True)

b=b.join(a,lsuffix='_left',rsuffix='_right')

b.to_csv('train2.csv',index=False)

