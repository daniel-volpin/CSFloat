SHELL := /bin/bash

.PHONY: help install lint format type fix run-backend run-frontend precommit init

help:
	@echo "Common targets:"
	@echo "  install       Install backend+frontend deps into current env"
	@echo "  lint          Run flake8 and ruff"
	@echo "  format        Run isort and black"
	@echo "  type          Run mypy"
	@echo "  fix           Autoflake, ruff --fix, isort, black"
	@echo "  run-backend   Start FastAPI (uvicorn)"
	@echo "  run-frontend  Start Streamlit app"
	@echo "  precommit     Install pre-commit hooks"

install:
	pip install -r backend/requirements.txt -r frontend/requirements.txt

lint:
	ruff check .
	flake8 .

format:
	isort .
	black .

type:
	mypy backend frontend

fix:
	autoflake --in-place --remove-all-unused-imports --remove-unused-variables --expand-star-imports -r .
	ruff check --fix .
	$(MAKE) format

run-backend:
	uvicorn backend.main:app --reload

run-frontend:
	cd frontend && streamlit run app.py

precommit:
	pre-commit install

