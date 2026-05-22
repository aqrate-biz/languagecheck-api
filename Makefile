PYTHON ?= .venv/bin/python

.PHONY: help install serve build check clean sync-openapi

help:
	@echo "Target disponibili:"
	@echo "  make install       Installa le dipendenze Python"
	@echo "  make serve         Avvia preview locale su http://127.0.0.1:8000"
	@echo "  make build         Esegue build locale"
	@echo "  make check         Esegue build strict (pre-deploy)"
	@echo "  make sync-openapi  Sincronizza openapi.yaml dentro docs/"
	@echo "  make clean         Rimuove la cartella site/"

install:
	$(PYTHON) -m pip install -r requirements.txt

serve:
	$(PYTHON) -m mkdocs serve

build:
	$(PYTHON) -m mkdocs build

check:
	$(PYTHON) -m mkdocs build --strict

sync-openapi:
	cp openapi.yaml docs/openapi.yaml

clean:
	rm -rf site