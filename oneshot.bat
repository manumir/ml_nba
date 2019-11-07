py update_data.py
cd .\logs
py calc.py
cd..
py get_today_games.py
py plac_preds.py
cd .\models
py linear_regression.py
py rf.py
cd..