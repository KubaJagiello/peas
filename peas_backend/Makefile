SOURCE_FILES := peas_app scripts
TEST_FILES := tests
APP := peas_app/api/app.py

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -r {} +
	rm -rf .pytest_cache

run-dev:
	poetry run fastapi --version
	poetry run fastapi dev $(APP)

test-cov:
	poetry run pytest --cov=$(SOURCE_FILES) $(TEST_FILES)

view-test-cov-html:
	poetry run pytest --cov=$(SOURCE_FILES) --cov-report=html $(TEST_FILES)
	open htmlcov/index.html

test:
	poetry run pytest $(TEST_FILES)

format:
	poetry run isort $(SOURCE_FILES) $(TEST_FILES)
	poetry run black $(SOURCE_FILES) $(TEST_FILES)

check:
	poetry run mypy $(SOURCE_FILES)

container-test:
	docker build -t peas-backend .
	docker run -it --rm -p 8000:8000 peas-backend
