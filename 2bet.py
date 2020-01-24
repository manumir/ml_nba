import pandas as pd

mlp=pd.read_csv('./logs/mlp_log.csv')
lin=pd.read_csv('./logs/linear_log.csv')
plac=pd.read_csv('./logs/plac_log.csv')
games=pd.read_csv('games.csv')

plac_preds=[]
for ix in range(len(games)+1):
  if plac.at[len(plac)-1-ix,'plac_H']>plac.at[len(plac)-1-ix,'plac_A']:
    plac_preds.append(1)
  else:
    plac_preds.append(0)

lin_preds=[]
for ix in range(len(games)+1):
  if float((lin.at[len(lin)-1-ix,'linear'])[1:-1])>0.49:
    lin_preds.append(1)
  else:
    lin_preds.append(0)

mlp_preds=[]
for ix in range(len(games)+1):
  if float((mlp.at[len(mlp)-1-ix,'mlp'])[1:-1])>0.5:
    mlp_preds.append(1)
  else:
    mlp_preds.append(0)

len_plac=len(plac)
print('lin:')
for i in range(len(plac_preds)):
  if plac_preds[i]!=lin_preds[i]:
    print(plac.at[len_plac-i-1,'home'],'@',plac.at[len_plac-i-1,'away'],'bet on',lin.at[len(lin)-i-1,'linear'])


print('\nmlp:')
for i in range(len(plac_preds)):
  if plac_preds[i]!=mlp_preds[i]:
    print(plac.at[len_plac-i-1,'home'],'@',plac.at[len_plac-i-1,'away'],'bet on',mlp.at[len(mlp)-i-1,'mlp'])
