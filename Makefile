.PHONY: default, lint

default:
	python -m kb
lint:
	pylint kb
pep8:
	autopep8 kb --in-place --recursive --aggressive --aggressive
test:
	pytest
reinstall:
	pip uninstall kb
	pyenv rehash
	pip install .
	pyenv rehash
