define USAGE
Possible Commands:
	venv			Creates virtual environment + runs it
	init      Install requirements with pip
	run     	Initialize database and then run app in dev environment.
endef

export USAGE
help:
	@echo "$$USAGE"

init:
	pip install -r requirements.txt

run:
	flask --app finance_tracker initdb
	flask --app finance_tracker run