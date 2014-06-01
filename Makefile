
.PHONY: test

ENV_NAME=apitest-env
BIN_DIR=$(CURDIR)/$(ENV_NAME)/bin

default: demo

install:
	virtualenv $(CURDIR)/$(ENV_NAME)
	$(BIN_DIR)/pip install -r $(CURDIR)/requirements.txt
	$(BIN_DIR)/python $(CURDIR)/setup.py develop
	$(BIN_DIR)/pip install -e $(CURDIR)/.

clean:
	rm -rf $(CURDIR)/$(ENV_NAME)
	rm -rf $(CURDIR)/src/apitest.egg-info

demo:
	$(MAKE) install
	$(BIN_DIR)/apitest demo

test:
	$(BIN_DIR)/nosetests $(CURDIR)/test/zato --with-coverage --cover-package=zato --nocapture
	$(BIN_DIR)/flake8 $(CURDIR)/src/zato --count
	$(BIN_DIR)/flake8 $(CURDIR)/test/zato --count
