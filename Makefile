.PHONY: all clean format format-check lint type test test-cov

CMD:=poetry run
PYMODULE:=ctff
TESTS:=tests
EXTRACODE:=

all: type test format lint

lint:
	$(CMD) ruff $(PYMODULE) $(TESTS) $(EXTRACODE)

lint-fix:
	$(CMD) ruff --fix $(PYMODULE) $(TESTS) $(EXTRACODE)


format:
	$(CMD) ruff format $(PYMODULE) $(TESTS) $(EXTRACODE)

format-check:
	$(CMD) ruff format --check $(PYMODULE) $(TESTS) $(EXTRACODE)

type:
	$(CMD) mypy $(PYMODULE) $(TESTS) $(EXTRACODE)

test:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS)

test-cov:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS) --cov-report html

clean:
	git clean -Xdf # Delete all files in .gitignore
