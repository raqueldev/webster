
VENV = venv
PYTHON ?= $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

virtualenv: SHELL := /bin/bash
virtualenv:
	virtualenv venv
	source venv/bin/activate

.PHONY: setup
setup:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	[[ -f webster/logs/webster.log ]] || touch webster/logs/webster.log && touch webster/logs/webster_error.log
	[[ -s webster/config/config.ini ]] || cp webster/config/config.ini.dist webster/config/config.ini
	@echo '**********************************************'
	@echo 'Installation has been done. '
	@echo 'Remember to configure your config file'

.PHONY: producer
producer:
	$(PYTHON) webster/producer.py

.PHONY: consumer
consumer:
	$(PYTHON) webster/consumer.py

.PHONY: run
run:
	$(PYTHON) webster/db_setup.py
	$(PYTHON) webster/webster.py
