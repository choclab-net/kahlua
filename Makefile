#!/usr/bin/make
# WARN: gmake syntax
########################################################
# Makefile for $(NAME)
#
# useful targets:
#	make check -- manifest checks
#	make clean -- clean distutils
#	make coverage_report -- code coverage report
#	make flake8 -- flake8 checks
#	make pylint -- source code checks
#	make sdist -- build python source distribution
#	make systest -- runs the system tests
#	make tests -- run all of the tests
#	make unittest -- runs the unit tests
#
# Notes:
# 1) flake8 is a wrapper around pep8, pyflakes, and McCabe.
########################################################
# variable section

PYTHON=python
COVERAGE=coverage
NOSE_OPTS = --with-coverage --cover-package=$(NAME)
SITELIB = $(shell $(PYTHON) -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")
VERSION = $(shell $(PYTHON) setup.py --version)
PACKAGES = home kahlua search
FLAKE8_IGNORE = W503

########################################################

all: clean check flake8 pylint tests

flake8:
	flake8 --ignore=$(FLAKE8_IGNORE) $(PACKAGES)
	flake8 --ignore=$(FLAKE8_IGNORE),E402 tests/

pylint:
	find $(PACKAGES) -not \( -path home/migrations -prune \) -name \*.py | xargs pylint --rcfile .pylintrc

bandit:
	bandit -r $(PACKAGES)

check:
	check-manifest

clean:
	@echo "Cleaning up distutils stuff"
	rm -rf build
	rm -rf dist
	rm -rf MANIFEST
	rm -rf *.egg-info
	@echo "Cleaning up byte compiled python stuff"
	find . -type f -regex ".*\.py[co]$$" -delete
	@echo "Cleaning up doc builds"
	rm -rf docs/_build
	rm -rf docs/api_modules
	rm -rf docs/client_modules
	@echo "Cleaning up test reports"
	rm -rf report/*

sdist: clean
	$(PYTHON) setup.py sdist

tests: unittest systest coverage_report

unittest: clean
	nosetests $(NOSE_OPTS) tests/unit/*

systest: clean
	nosetests $(NOSE_OPTS) tests/system/*

integration:
	@echo "running behavioural integration tests"

smoke:
	@echo "running smoke tests"

load:
	@echo "running load tests"

coverage_report:
	$(COVERAGE) report --rcfile=".coveragerc"
