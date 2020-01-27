import pandas as pd

mlp=pd.read_csv('./logs/mlp_log.csv')
lin=pd.read_csv('./logs/linear_log.csv')
plac=pd.read_csv('./logs/plac_log.csv')
games=pd.read_csv('games.csv')

# plac
plac=plac[-len(games):]
plac.reset_index(drop=True,inplace=True)

plac_preds=[]
for ix in range(len(games)):
  if plac.at[ix,'plac_H']>plac.at[ix,'plac_A']:
    plac_preds.append(1)
  else:
    plac_preds.append(0)

# lin
lin=lin[-len(games):]
lin.reset_index(drop=True,inplace=True)

lin_preds=[]
for ix in range(len(games)):
  if float((lin.at[ix,'linear'])[1:-1])>0.49:
    lin_preds.append(1)
  else:
    lin_preds.append(0)

# mlp
mlp=mlp[-len(games):]
mlp.reset_index(drop=True,inplace=True)

mlp_preds=[]
for ix in range(len(games)):
  if float((mlp.at[ix,'mlp'])[1:-1])>0.5:
    mlp_preds.append(1)
  else:
    mlp_preds.append(0)

# print stuff
len_plac=len(plac)
print('lin:')
for i in range(len(games)):
  if plac_preds[i]!=lin_preds[i]:
    print(plac.at[i,'home'],'vs',plac.at[i,'away'],'bet on',lin.at[i,'linear'])

print('\nmlp:')
for i in range(len(plac_preds)):
  if plac_preds[i]!=mlp_preds[i]:
    print(plac.at[i,'home'],'vs',plac.at[i,'away'],'bet on',mlp.at[i,'mlp'])
