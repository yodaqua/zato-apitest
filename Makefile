
ENV_NAME=apitest

default: demo

install:
	virtualenv $(CURDIR)/$(ENV_NAME)
	$(CURDIR)/$(ENV_NAME)/bin/pip install -r $(CURDIR)/requirements.txt
	$(CURDIR)/$(ENV_NAME)/bin/python $(CURDIR)/setup.py develop
	$(CURDIR)/$(ENV_NAME)/bin/pip install -e $(CURDIR)/.

clean:
	rm -rf $(CURDIR)apitest
	rm -rf $(CURDIR)src/apitest.egg-info

demo:
	$(MAKE) install
	$(CURDIR)/apitest/bin/apitest demo