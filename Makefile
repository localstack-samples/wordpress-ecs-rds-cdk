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
	ln -sfn `pwd`/node_modules/aws-cdk-local/bin/cdklocal $(VENV_DIR)/bin/

deploy-local:
	$(VENV_RUN); \
	cd deployments/cdk; \
	cdklocal bootstrap || true; \
	cdklocal deploy --all --require-approval never

destroy-local:
	$(VENV_RUN); \
	cd deployments/cdk; \
	cdklocal destroy --all

format:
	$(VENV_ACTIVATE); python -m isort .; python -m black .

.PHONY: clean format install deploy
