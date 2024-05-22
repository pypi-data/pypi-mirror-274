all:
	echo "Please check the Makefile for available targets"

VERSION := '$(shell python3 version.py)'
TAG := 'egenix-micro-benchmark-$(VERSION)'

### Prepare the virtual env

install-pyrun:
	install-pyrun pyenv

install-venv:
	python3.11 -m venv pyenv

install-packages:
	pip install -r requirements.txt

install-dev-packages:
	pip install -r requirements.txt -r requirements-dev.txt

uninstall-packages:
	pip uninstall -y -r requirements.txt

update-packages:
	pip-sync

pip-compile:
	pip-compile -o requirements.txt pyproject.toml
	pip-compile --extra dev -o requirements-dev.txt pyproject.toml

### Code

check-code:
	ruff check micro_benchmark

### Build

clean:
	find . \( -name '*~' -or -name '*.bak' \) -exec rm {} ';'

distclean:	clean
	rm -rf build dist *.egg-info __pycache__

update-version:
	$(EDITOR) micro_benchmark/__init__.py

create-dist:	distclean
	echo "Building distributions for version $(VERSION)"
	python3 -m build

tag-release:
	git tag -a $(TAG) -m "Release $(VERSION)"
	git push origin --tags

test-upload:
	python3 -m twine upload -r testpypi dist/*$(VERSION).tar.gz
	python3 -m twine upload -r testpypi dist/*$(VERSION)-py*.whl

prod-upload:
	python3 -m twine upload dist/*$(VERSION).tar.gz
	python3 -m twine upload dist/*$(VERSION)-py*.whl
	cp dist/*$(VERSION).tar.gz ~/projects/archives

### Run

run:
	python3 -m examples.bench_example
	python3 -m examples.bench_match
