PYTHON = python
TEST = pytest
TYPE_CHECK = mypy --strict
STYLE_CHECK = flake8
STYLE_FIX = autopep8 --in-place
PDOC = pdoc

SOURCE_FILES = point.py polygon.py convexpolygonarea.py
TEST_FILES = tests/test_point.py tests/test_polygon.py tests/test_convexpolygonarea.py

.PHONY: all
all: check-style check-type unit-test program-test
	@echo "All assignment checks passed"

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
	@set -e; \
	for input in data/*.in; do \
		answer=$${input%.in}.ans; \
		echo "Testing $$input"; \
		$(PYTHON) convexpolygonarea.py < $$input | diff -u $$answer -; \
	done
	@echo "All program tests passed"

.PHONY: coverage
coverage:
	$(TEST) --cov=point --cov=polygon --cov=convexpolygonarea \
		--cov-report=term-missing tests

.PHONY: docs
docs:
	rm -rf docs
	mkdir -p docs
	$(PDOC) -o docs ./point.py ./polygon.py ./convexpolygonarea.py
	rm -f docs/.gitignore

.PHONY: kattis-test
kattis-test:
	kattis test

.PHONY: clean
clean:
	rm -rf .pytest_cache .mypy_cache htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -f .coverage
