cd .\logs
py calc.py
py bets_simulation.py
cd..
py update_data.py
cd .\logs
py calc.py
py bets_simulation.py
cd..
py get_today_games.py
py plac_preds.py
cd .\models
py linear_regression.py
py mlp.py
py svm.py
py xgb.py
py trees.py
py rf.py
cd..
