.PHONY: install test lint typecheck audit verify run docker

install:
	python -m pip install -r requirements-dev.lock
	python -m pip install -e . --no-deps

test:
	pytest -q

lint:
	ruff check .

typecheck:
	mypy src

audit:
	pip-audit -r requirements.lock

verify:
	python scripts/verify_reproducibility.py

run:
	uvicorn reconforge.main:app --host 0.0.0.0 --port 8000

docker:
	docker compose up --build
