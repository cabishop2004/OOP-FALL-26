PYTHON = python
TEST = pytest
TYPE_CHECK = mypy --strict
STYLE_CHECK = flake8
STYLE_FIX = autopep8 --in-place
PDOC = pdoc

SOURCE_FILES = weather.py weather_client.py weather_adapter.py weather_manager.py
TEST_FILES = \
	tests/test_weather.py \
	tests/test_weather_client.py \
	tests/test_weather_adapter.py \
	tests/test_weather_manager.py

.PHONY: all
all: check-style check-type unit-test coverage
	@echo "All configured Assignment 3 checks passed"

.PHONY: check-style
check-style:
	$(STYLE_CHECK) $(SOURCE_FILES) tests

.PHONY: fix-style
fix-style:
	$(STYLE_FIX) $(SOURCE_FILES) $(TEST_FILES)

.PHONY: check-type
check-type:
	$(TYPE_CHECK) $(SOURCE_FILES) $(TEST_FILES)

.PHONY: unit-test
unit-test:
	$(TEST) -v tests

.PHONY: program-test
program-test:
	kattis test

.PHONY: kattis-test
kattis-test:
	kattis test

.PHONY: coverage
coverage:
	$(TEST) \
		--cov=weather \
		--cov=weather_client \
		--cov=weather_adapter \
		--cov=weather_manager \
		--cov-report=term-missing \
		--cov-fail-under=100 \
		tests

.PHONY: api-test
api-test:
	$(PYTHON) weather.py 39.0639 -108.5506

.PHONY: docs
docs:
	rm -rf docs
	mkdir -p docs
	$(PDOC) -o docs \
		./weather.py \
		./weather_client.py \
		./weather_adapter.py \
		./weather_manager.py
	rm -f docs/.gitignore

.PHONY: clean
clean:
	rm -rf .pytest_cache .mypy_cache .hypothesis htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -f .coverage
