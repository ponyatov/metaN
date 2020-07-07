CWD     = $(CURDIR)
MODULE  = $(notdir $(CWD))
OS     ?= $(shell uname -s)

PIP = $(CWD)/bin/pip3
PY  = $(CWD)/bin/python3

all: $(MODULE).log
$(MODULE).log: $(PY) $(MODULE).py $(MODULE).ini
	$^ > $@



$(PIP) $(PY):
	python3 -m venv .
	$(PIP) install -U pip pylint autopep8
	$(MAKE) requirements.txt

.PHONY: requirements.txt
requirements.txt: $(PIP)
	$< freeze | grep -v 0.0.0 > $@



.PHONY: master shadow release

MERGE  = Makefile README.md .gitignore .vscode apt.txt requirements.txt
MERGE += $(MODULE).py $(MODULE).ini

master:
	git checkout $@
	git pull -v
	git checkout shadow -- $(MERGE)

shadow:
	git checkout $@
	git pull -v

release:
	git tag $(NOW)-$(REL)
	git push -v && git push -v --tags
	$(MAKE) shadow
