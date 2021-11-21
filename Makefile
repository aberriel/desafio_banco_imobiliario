define UNINSTALL_ALL_PYSCRIPT
import os
from requirements import requirements
os.system('pip uninstall --yes %s' % ' '.join([x.split('==')[0] for x in requirements]))
endef

export UNINSTALL_ALL_PYSCRIPT

uninstall_all: ## uninstall all packages listed on requirements
	@python -c "$$UNINSTALL_ALL_PYSCRIPT"

clean: clean-build clean-pyc

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

tests: ## Test and lint
	python3 -m pytest $(CAPTURE) --cov=tests --cov=src -W ignore::DeprecationWarning --cov-report term-missing:skip-covered
	@echo "Linting..."
	@flake8 src/ --max-complexity=5
	@flake8 tests/ --ignore=S101,S311,F811 --max-complexity=5
	@echo "\033[32mTudo certo!"

install: clean uninstall_all ## install the package to the active Python's site-packages
	pip install -r requirements.txt