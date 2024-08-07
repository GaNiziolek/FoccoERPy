python-venv:
	python -m venv .venv

install: python-venv
	. .venv/bin/activate ;\
	pip install --editable ".[dev]"
