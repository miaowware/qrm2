# A quick installation script for discord bots.
#
# Copyright (c) 2019 0x5c
# Released under the terms of the MIT license.
#
# https://github.com/0x5c/discord.py-quickinstall


#### Setup ####
.DEFAULT_GOAL := help

## Variables ##
# Those are the defaults; they can be over-ridden if specified
# at en environment level or as 'make' arguments.
BOTENV ?= botenv
PY3DOT ?= 7
PIP_OUTPUT ?= q


# Define some rules as phony
.PHONY: help install clean onlyenv



#### Targets ####

## Support targets ##

help:
	@echo ""
	@echo "\033[97m>>>>>>  Default dummy target  <<<<<<"
	@echo "\033[37mYou might want to specify a target:"
	@echo "\033[32m    --> make install"
	@echo "\033[94m    --> make clean"
	@echo "\033[0m"


## Actual install/setup targets ##

# Main install target
install: $(BOTENV)/req_done options.py keys.py

# Virual environment setup
$(BOTENV)/success:
ifneq ("$(wildcard ./$(BOTENV).)",)
	@echo "\033[94m--> Creating the virtual environment...\033[0m"
	@python3.$(PY3DOT) -m venv $(BOTENV)
	@touch $(BOTENV)/success
endif

# Installing requirements
$(BOTENV)/req_done: requirements.txt $(BOTENV)/success
	@echo "\033[34;1m--> Installing the dependencies...\033[0m"
	@. $(BOTENV)/bin/activate; \
	pip install -${PIP_OUTPUT} -U pip setuptools wheel; \
	pip install -${PIP_OUTPUT} -U -r requirements.txt
	@touch $(BOTENV)/req_done

# Copying templates
options.py keys.py:
	@echo "\033[34;1m--> Copying template files...\033[0m"
	@cp -nv ./templates/template_$@ ./$@
	@touch ./$@

# Deletes the python cache and the virtual environment
clean:
	@echo "\033[34;1m--> Removing python cache files...\033[0m"
	rm -rf __pycache__
	@echo "\033[34;1m--> Removing the virtual environment...\033[0m"
	rm -rf $(BOTENV)


## Dev targets ##


## Weird dev targets ##
onlyenv: $(BOTENV)/success
