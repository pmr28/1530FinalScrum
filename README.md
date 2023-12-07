# 1530 FinalScrum

## Financial Tracking Application
Product Owner: Paul Ringenbach (Sprint 1) / Emily Kyle (Sprint 2)  
Scrum Master: Matthew Mell (Sprint 1) / Nicole Poliski (Sprint 2)

All scrum documentation and deployment diagram located in the PDF in the repo.

## Installing
Download and extract the zip file from the main repo somehwere on your machine
Python must be installed to run

### How To Run on MacOS
##### In terminal in project folder:
1. `python3 -m venv .venv`
2. `. .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `flask --app finance_tracker initdb`
5. `flask --app finance_tracker run`

OR 
##### Use the makefile (still in terminal in project folder): 
1. `python3 -m venv .venv`
2. `. .venv/bin/activate`
3. `make init`
4. `make run`

### How To Run on Windows
##### In terminal in project folder:
1. `python -m venv .`
2. `.\Scripts\activate`
3. `pip install flask flask-sqlalchemy`
4. `flask --app finance_tracker initdb`
5. `flask --app finance_tracker run`

## How to Run Unit Test
### Windows
`python test_expenses.py`
### MacOS
`python3 test_expenses.py`

