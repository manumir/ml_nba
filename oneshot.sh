cd logs
python3 calc.py
python3 bets_simulation.py
cd ..
python3 update_data.py
cd logs
python3 calc.py
python3 bets_simulation.py
cd ..
python3 get_today_games.py
python3 plac_preds.py
cd models
python3 linear_regression.py
python3 mlp.py
python3 svm.py
python3 xgb.py
#py trees.py #too much timee to run
#py rf.py #too much timee to run
cd ..
