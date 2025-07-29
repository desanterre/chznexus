.PHONY: install run clean shell black isort test

install:
	poetry install

shell:
	poetry shell

run:
	poetry run uvicorn chznexus.app:app --reload

black:
	poetry run black .

isort:
	poetry run isort .

lint: black . isort .

test:
	PYTHONPATH=. poetry run pytest

clean:
	rm -rf __pycache__ .pytest_cache
	find . -name "*.pyc" -delete
