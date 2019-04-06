test:
	pipenv run pytest -v
	$(eval COV_DIR := $(shell pwd))
	@echo To confirm: $(COV_DIR)/htmlcov/index.html
dep:
	pipenv install

.PHONY: all build clean test
