# This file has been auto-generated.
# All manual changes may be lost, see Projectfile.
#
# Date: 2016-02-13 18:20:43.900370

PYTHON ?= $(shell which python)
PYTHON_BASENAME ?= $(shell basename $(PYTHON))
PYTHON_REQUIREMENTS_FILE ?= requirements.txt
QUICK ?= 
VIRTUALENV_PATH ?= .$(PYTHON_BASENAME)-virtualenv
WHEELHOUSE_PATH ?= .$(PYTHON_BASENAME)-wheelhouse
PIPCACHE_PATH ?= .$(PYTHON_BASENAME)-pipcache
PIP ?= $(VIRTUALENV_PATH)/bin/pip --cache-dir=$(PIPCACHE_PATH)
PYTEST_OPTIONS ?= --capture=no --cov=edgy/workflow --cov-report html

.PHONY: clean install lint test

# Installs the local project dependencies, using the environment given requirement file.
install: $(VIRTUALENV_PATH)
	if [ -z "$(QUICK)" ]; then \
	    $(PIP) wheel -w $(WHEELHOUSE_PATH) -f $(WHEELHOUSE_PATH) -r $(PYTHON_REQUIREMENTS_FILE); \
	    $(PIP) install -f $(WHEELHOUSE_PATH) -U -r $(PYTHON_REQUIREMENTS_FILE); \
	fi

# Setup the local virtualenv.
$(VIRTUALENV_PATH):
	virtualenv -p $(PYTHON) $(VIRTUALENV_PATH)
	$(VIRTUALENV_PATH)/bin/pip install -U pip\>=8.0,\<9.0 wheel\>=0.24,\<1.0
	ln -fs $(VIRTUALENV_PATH)/bin/activate $(PYTHON_BASENAME)-activate

clean:
	rm -rf $(VIRTUALENV_PATH) $(WHEELHOUSE_PATH) $(PIPCACHE_PATH)

lint: install
	$(VIRTUALENV_PATH)/bin/pylint --py3k edgy.workflow -f html > pylint.html

test: install
	$(VIRTUALENV_PATH)/bin/py.test $(PYTEST_OPTIONS) tests
