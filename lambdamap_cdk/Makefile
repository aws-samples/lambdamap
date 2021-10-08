export SHELL
SHELL:=/bin/bash
ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

.PHONY: deploy

# create the virtual environment from which to run each target
.venv: requirements.txt
	python3 -B -m venv $@
	source $@/bin/activate ; pip install -r $<

deploy: app.py .venv
	source $(word 2, $^)/bin/activate ; \
	cdk deploy -a 'python3 -B $<'