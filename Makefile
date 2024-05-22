# REF: https://github.com/rochacbruno/python-project-template/blob/main/Makefile

.ONESHELL:
ENV_PREFIX=$(shell poetry env info --path)/bin
PROJECT_NAME=$(shell invoke const.project-name)

.PHONY: help
help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep


.PHONY: show
show:             ## Show the current environment.
	@echo "Current environment:"
	@poetry env info

.PHONY: deps
deps:             ## Install dependencies of project.
	@echo "List commnd paths or install if not found"
	which pip || sudo apt install python3-pip
	which poetry || python3 -m pip install poetry
	which invoke || python3 -m pip install invoke
	which yasha || python3 -m pip install yasha
	poetry config --local virtualenvs.in-project trues
	poetry install --no-root
	invoke deps.install-post-bootstrap

.PHONY: install
install:          ## Install the project in dev mode.
	poetry install

.PHONY: fmt
fmt:              ## Format code using black & isort.
	$(ENV_PREFIX)isort ${PROJECT_NAME}/
	$(ENV_PREFIX)black -l 79 ${PROJECT_NAME}/
	$(ENV_PREFIX)black -l 79 tests/

.PHONY: lint
lint:             ## Run pep8, black, mypy linters.
	$(ENV_PREFIX)flake8 ${PROJECT_NAME}/
	$(ENV_PREFIX)black -l 79 --check ${PROJECT_NAME}/
	$(ENV_PREFIX)black -l 79 --check tests/
	$(ENV_PREFIX)mypy --ignore-missing-imports ${PROJECT_NAME}/

.PHONY: test
test: lint        ## Run tests and generate coverage report.
	$(ENV_PREFIX)pytest -v --cov-config .coveragerc --cov=${PROJECT_NAME} -l --tb=short --maxfail=1 tests/
	$(ENV_PREFIX)coverage xml
	$(ENV_PREFIX)coverage html

.PHONY: watch
watch:            ## Run tests on every change.
	ls **/**.py | entr $(ENV_PREFIX)pytest -s -vvv -l --tb=long --maxfail=1 tests/

.PHONY: clean
clean:            ## Clean unused files.
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build

.PHONY: docs
docs:             ## Build the documentation.
	@echo "building documentation ..."
	@$(ENV_PREFIX)mkdocs build
	URL="site/index.html"; xdg-open $$URL || sensible-browser $$URL || x-www-browser $$URL || gnome-open $$URL || open $$URL

.PHONY: build
docker:           ## Make docker files and all deps
	invoke build.j2
	docker compose build