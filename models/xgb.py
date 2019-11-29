import pandas as pd
import functions as f
import os
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

curr_path=os.getcwd()
path2data=curr_path[:-6]
path2logs=curr_path[:-6]+'\\logs\\'
log=pd.read_csv(path2logs+'xgb_log.csv')


# load data
data=pd.read_csv(path2data+'train.csv')
data=data.dropna()
data=data.drop(['Team_home','Match Up_home','Game Date_home','Team_away',
           'Match Up_away','Game Date_away','MIN_home','MIN_away',
           'W/L_home','W/L_away'],1)
Y=data.pop('Result')
X=data

# split data into train and test sets
X_train,X_test,y_train,y_test = train_test_split(X, Y, test_size=0.2, random_state=7)

# fit model no training data
model = xgb.XGBRegressor()
model.fit(X_train, y_train)

# make predictions for test data
y_pred = model.predict(X_test)
predictions = [round(value) for value in y_pred]
print('zeros:',f.get0and1(y_pred))
# evaluate predictions
accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))

df2log['xgb']=y_pred
df2log=df2log.sort_values('home')
log=log.append(df2log,sort=False)
log.to_csv(path2logs+'xgb_log.csv',index=False)
