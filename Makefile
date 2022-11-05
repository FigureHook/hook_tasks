.PHONY: help
.SILENT:

help: # Show this help message.
	@grep -E '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

lint: # Lint the code.
	flake8

type-check: # Type check with mypy.
	mypy

format: # Format the code.
	isort -e .; \
	black .

unit-tests: # Run the unit-tests.
	coverage run -m pytest -k "unit_tests"; \
	coverage combine; \
	coverage report --precision=2 -m

integration-tests: # Run the integration-tests.
	coverage run -m pytest -k "integration_tests"; \
	coverage combine; \
	coverage report --precision=2 -m

freeze: # Export the requirements.txt file.
	poetry export --without-hashes -f requirements.txt --output requirements.txt

freeze-dev: # Export the requirements.dev.txt file.
	poetry export --without-hashes --dev -f requirements.txt --output requirements.dev.txt
