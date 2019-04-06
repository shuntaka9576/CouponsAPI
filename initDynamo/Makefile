test:
	pipenv run pytest -p no:warnings --capture=no -v --cov=app/ --cov-report=html
	$(eval COV_DIR := $(shell pwd))
	@echo To confirm: $(COV_DIR)/htmlcov/index.html
dep:
	pipenv install

.PHONY: all build clean test
