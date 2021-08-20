.PHONY: format test-all

test-all:
	nosetests tests

format:
	black --config black.toml .