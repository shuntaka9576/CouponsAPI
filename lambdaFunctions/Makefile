test:
	pipenv run pytest -v
	$(eval COV_DIR := $(shell pwd))
	@echo To confirm: $(COV_DIR)/htmlcov/index.html
clean:
	-rm -rf ./.venv
dep: clean
	pipenv install
dep-dev: clean
	pipenv install --dev

.PHONY: all build clean test
