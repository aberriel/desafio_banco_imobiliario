#!/bin/bash
echo 'Setando a virtualenv'
source virtualenv/bin/activate
echo 'Executando testes'

python3 -m pytest $(CAPTURE) --cov=tests --cov=src -W ignore::DeprecationWarning --cov-report term-missing:skip-covered
@echo "Linting..."
@flake8 src/ --max-complexity=5
@flake8 tests/ --ignore=S101,S311,F811 --max-complexity=5
@echo "\033[32mTudo certo!"