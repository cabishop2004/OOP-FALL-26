PYTHON = python
TEST = pytest
TYPE_CHECK = mypy --strict
STYLE_CHECK = flake8
STYLE_FIX = autopep8 --in-place
PDOC = pdoc
BANDIT = bandit

SOURCE_FILES = fraction.py formatter.py mixedfractions.py
TEST_FILES = tests/test_fraction.py tests/test_formatter.py tests/test_mixedfractions.py

.PHONY: all
all: check-style check-type unit-test program-test coverage
	@echo "All Assignment 2 checks passed"

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
		$(PYTHON) mixedfractions.py < $$input | diff -u $$answer -; \
	done
	@echo "All program tests passed"

.PHONY: kattis-test
kattis-test:
	kattis test

.PHONY: coverage
coverage:
	$(TEST) \
		--cov=fraction \
		--cov=formatter \
		--cov=mixedfractions \
		--cov-report=term-missing \
		--cov-fail-under=100 \
		tests

.PHONY: security
security:
	$(BANDIT) -r $(SOURCE_FILES)

.PHONY: docs
docs:
	rm -rf docs
	mkdir -p docs
	$(PDOC) -o docs ./fraction.py ./formatter.py ./mixedfractions.py
	rm -f docs/.gitignore

.PHONY: clean
clean:
	rm -rf .pytest_cache .mypy_cache .hypothesis htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -f .coverage
