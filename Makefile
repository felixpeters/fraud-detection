clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -f .coverage
	rm -f .coverage.*
	rm -rf htmlcov

clean: clean-pyc clean-test

build:
	pip install -e .

test: clean
	pytest --cov=. --cov-report=html --cov-report=term-missing --disable-pytest-warnings tests/

test-pipeline: clean
	pytest --doctest-modules --junitxml=junit/test-results.xml --cov=. --cov-report=xml --disable-pytest-warnings tests/