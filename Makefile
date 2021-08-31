.PHONY: format test-all test-cover

test-all:
	nosetests tests

test-cover:
	nosetests --with-coverage --cover-package=hzkerberos tests

format:
	black --config black.toml .
