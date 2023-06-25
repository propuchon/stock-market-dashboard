start:
	python main.py

install:
	pip install -U -r requirements.txt

format:
	autoflake -i --remove-all-unused-imports --ignore-init-module-imports --expand-star-imports --exclude venv -r .
	isort .
	black .
