# A quick installation script for painless discord bots.
# v2.0.0
# Copyright (c) 2019 0x5c
# Released under the terms of the MIT license.
# Part of:
# https://github.com/0x5c/quick-bot-no-pain


.DEFAULT_GOAL := help

### Variables ###
# Those are the defaults; they can be over-ridden if specified
# at en environment level or as 'make' arguments.
BOTENV ?= botenv
PYTHON_BIN ?= python3.7
PIP_OUTPUT ?= -q


### Support targets ###

.PHONY: help
help:
	@echo ""
	@echo "\033[97m>>>>>>  Default dummy target  <<<<<<"
	@echo "\033[37mYou might want to specify a target:"
	@echo "\033[32m    --> make install"
	@echo "\033[94m    --> make clean"
	@echo "\033[0m"


### Actual install/setup targets ###

# Main install target
.PHONY: install
install: $(BOTENV)/req_done data/options.py data/keys.py

# Virual environment setup
$(BOTENV)/success:
ifneq ("$(wildcard ./$(BOTENV).)",)
	@echo "\033[94m--> Creating the virtual environment...\033[0m"
	@$(PYTHON_BIN) -m venv $(BOTENV)
	@touch $(BOTENV)/success
endif

# Installing requirements
$(BOTENV)/req_done: requirements.txt $(BOTENV)/success
	@echo "\033[34;1m--> Installing the dependencies...\033[0m"
	@. $(BOTENV)/bin/activate; \
		pip install ${PIP_OUTPUT} -U pip setuptools wheel; \
		pip install ${PIP_OUTPUT} -U -r requirements.txt
	@touch $(BOTENV)/req_done

# Creating the ./data subdirectory
data:
	@echo "\033[34;1m--> Creating ./data ...\033[0m"
	@mkdir -p data

# Copying templates
data/options.py data/keys.py: ./data
	@echo "\033[34;1m--> Copying template for ./$@ ...\033[0m"
	@cp -nv ./templates/$@ ./$@
	@touch ./$@

# Deletes the python cache and the virtual environment
.PHONY: clean
clean:
	@echo "\033[34;1m--> Removing python cache files...\033[0m"
	rm -rf __pycache__
	@echo "\033[34;1m--> Removing the virtual environment...\033[0m"
	rm -rf $(BOTENV)


### Dev targets ###


### Special targets ###
.PHONY: onlyenv
onlyenv: $(BOTENV)/success
