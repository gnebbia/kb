.PHONY: default, lint

default:
	python -m kb
lint:
	pylint kb
pep8:
	autopep8 kb --in-place --recursive --aggressive --aggressive
clean:
	rm -rf build/ dist/
test:
	pytest
