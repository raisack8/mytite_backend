echo "--------- Django server run!!!"
call venv/Scripts/activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py runserver