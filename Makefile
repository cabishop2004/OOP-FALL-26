A1 = assignments/A1-OOD/convexpolygonarea

.PHONY: all
all: check-style check-type run-test program-test
	@echo "All global checks passed"

.PHONY: check-style
check-style:
	$(MAKE) -C $(A1) check-style

.PHONY: fix-style
fix-style:
	$(MAKE) -C $(A1) fix-style

.PHONY: check-type
check-type:
	$(MAKE) -C $(A1) check-type

.PHONY: run-test
run-test:
	$(MAKE) -C $(A1) unit-test

.PHONY: program-test
program-test:
	$(MAKE) -C $(A1) program-test

.PHONY: coverage
coverage:
	$(MAKE) -C $(A1) coverage

.PHONY: docs
docs:
	$(MAKE) -C $(A1) docs

.PHONY: clean
clean:
	$(MAKE) -C $(A1) clean
	find . -type d -name .hypothesis -prune -exec rm -rf {} +
