.PHONY: all clean lint type test test-cov

CMD:=poetry run
PYMODULE:=ctff
TESTS:=tests
EXTRACODE:=

all: type test lint

lint:
	$(CMD) ruff $(PYMODULE) $(TESTS) $(EXTRACODE)

type:
	$(CMD) mypy $(PYMODULE) $(TESTS) $(EXTRACODE)

test:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS)

test-cov:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS) --cov-report html

clean:
	git clean -Xdf # Delete all files in .gitignore
