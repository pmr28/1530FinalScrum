# 1530FinalScrum

## Financial Tracking Application
Product Owner: Paul Ringenbach(Sprint 1) / Emily Kyle (Sprint 2)  
Scrum Master: Matthew Mell(Sprint 1) / Nicole Poliski(Sprint 2)

## Installing
Python must be installed

### How To Run on MacOS
##### In terminal in project folder:
1. "python3 -m venv .venv"
2. ". .venv/bin/activate"
3. "pip install -r requirements.txt"
4. "flask --app finance_tracker initdb"
5. "flask --app finance_tracker run"

OR 
##### Use the makefile (still in terminal in project folder): 
1. "python3 -m venv .venv"
2. Mac: ". .venv/bin/activate"  
   Windows: ". .venv\Scripts\activate"
2. "make init"
3. "make run"

### How To Run on Windows
##### In terminal in project folder:
1. "python -m venv ."
2. ". .venv\Scripts\activate"
3. "pip install flask flask-sqlalchemy"
4. "flask --app finance_tracker initdb"
5. "flask --app finance_tracker run"
