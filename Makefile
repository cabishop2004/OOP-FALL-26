A1 = assignments/A1-OOD/convexpolygonarea
A2 = assignments/A2-decorator/mixedfractions

.PHONY: all
all: check-style check-type run-test program-test security
	@echo "All global checks passed"

.PHONY: check-style
check-style:
	$(MAKE) -C $(A1) check-style
	$(MAKE) -C $(A2) check-style

.PHONY: fix-style
fix-style:
	$(MAKE) -C $(A1) fix-style
	$(MAKE) -C $(A2) fix-style

.PHONY: check-type
check-type:
	$(MAKE) -C $(A1) check-type
	$(MAKE) -C $(A2) check-type

.PHONY: run-test
run-test:
	$(MAKE) -C $(A1) unit-test
	$(MAKE) -C $(A2) unit-test

.PHONY: program-test
program-test:
	$(MAKE) -C $(A1) program-test
	$(MAKE) -C $(A2) program-test

.PHONY: security
security:
	$(MAKE) -C $(A2) security

.PHONY: coverage
coverage:
	$(MAKE) -C $(A1) coverage
	$(MAKE) -C $(A2) coverage

.PHONY: docs
docs:
	$(MAKE) -C $(A1) docs
	$(MAKE) -C $(A2) docs

.PHONY: clean
clean:
	$(MAKE) -C $(A1) clean
	$(MAKE) -C $(A2) clean
	find . -type d -name .hypothesis -prune -exec rm -rf {} +
