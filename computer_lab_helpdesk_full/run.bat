@echo off
python -m pip install -r requirements.txt
python ml_model\train_model.py
python backend\app.py
pause
