#
# USAGE:
# 	make deploy MEMORY=512 TIMEOUT=30 EXTRA_CMDS='pip install pandas'
#
export SHELL
SHELL:=/bin/bash
ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

STACK_NAME:=LambdaMapStack
FUNCTION_NAME:=LambdaMapFunction

# memory in MB
MEMORY:=256

# timeout in seconds
TIMEOUT:=900

CDK_TAGS:=--tags Project=lambdamap

# Use `EXTRA_CMDS` to run custom commands with the `RUN` instruction in
# the lambda container Dockerfile. This is useful for installing custom
# libraries you want made available in the lamda container, e.g: 
#
# 	EXTRA_CMDS='pip install pandas scikit-learn'
# 
# which will make the `pandas` and `sklearn` python packages available to the
# python function you want to run on lambdamap.
EXTRA_CMDS:=

.PHONY: tests health

.venv: requirements.txt
	python3 -B -m venv $@
	source $@/bin/activate ; pip install -r $<

tests: .venv
	source $</bin/activate ; \
	PYTHONPATH=.:lambdamap_cdk pytest -vs tests/

health: .venv
	source $</bin/activate ; \
	PYTHONPATH=.:lambdamap_cdk python tests/bin/health.py

bootstrap: .venv
	source $</bin/activate ; \
	export AWS_REGION=$$(aws ec2 describe-availability-zones --output text --query 'AvailabilityZones[0].[RegionName]') ; \
	export AWS_ACCOUNT_ID=$$(aws sts get-caller-identity --query Account --output text) ; \
	cdk bootstrap aws://$$AWS_ACCOUNT_ID/$$AWS_REGION

deploy: lambdamap_cdk/app.py .venv
	source $(word 2, $^)/bin/activate ; \
	export PYTHONDONTWRITEBYTECODE=1 ; \
	cdk deploy -a 'python3 -B $<' \
		-c stack_name=${STACK_NAME} \
		-c function_name=${FUNCTION_NAME} \
		-c memory_size=${MEMORY} \
		-c timeout_secs=${TIMEOUT} \
		-c extra_cmds=${EXTRA_CMDS} \
		--require-approval never \
		${CDK_TAGS}