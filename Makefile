export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION=us-east-1
SHELL := /bin/bash

usage:		## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

start:		## Start LocalStack
	@test -n "${LOCALSTACK_AUTH_TOKEN}" || (echo "LOCALSTACK_AUTH_TOKEN is not set. Find your token at https://app.localstack.cloud/workspace/auth-token"; exit 1)
	@LOCALSTACK_AUTH_TOKEN=$(LOCALSTACK_AUTH_TOKEN) lstk start

stop:		## Stop LocalStack
	@lstk stop


logs:		## Save the logs in a separate file
	@lstk logs > logs.txt

VENV_BIN = python3 -m venv
VENV_DIR ?= .venv
VENV_ACTIVATE = $(VENV_DIR)/bin/activate
VENV_RUN = . $(VENV_ACTIVATE)

venv: $(VENV_ACTIVATE)

$(VENV_ACTIVATE): setup.py setup.cfg pyproject.toml
	test -d .venv || $(VENV_BIN) .venv
	$(VENV_RUN); pip install --upgrade pip setuptools wheel
	$(VENV_RUN); pip install -e .[dev,deploy]
	touch $(VENV_DIR)/bin/activate

clean:
	rm -rf .venv
	rm -rf build/
	rm -rf .eggs/
	rm -rf *.egg-info/
	rm -rf node_modules
	rm -rf deployments/cdk/cdk.out

install: venv
	npm install; \
	ln -sfn `pwd`/node_modules/aws-cdk/bin/cdk $(VENV_DIR)/bin/; \
	which lstk || npm install -g @localstack/lstk

deploy-local:
	$(VENV_RUN); \
	cd deployments/cdk; \
	lstk cdk bootstrap || true; \
	lstk cdk deploy --all --require-approval never

deploy-aws:
	$(VENV_RUN); \
	cd deployments/cdk; \
	cdk bootstrap || true; \
	cdk deploy --all --require-approval never

destroy-local:
	$(VENV_RUN); \
	cd deployments/cdk; \
	lstk cdk destroy --all

destroy-aws:
	$(VENV_RUN); \
	cd deployments/cdk; \
	cdk destroy --all

format:
	$(VENV_ACTIVATE); python -m isort .; python -m black .

.PHONY: clean format install deploy
