install:
	python setup.py install
	pre-commit install --install-hooks && pre-commit autoupdate

format:
	black src tests scripts

clean_tests:
	rm -rf .pytest_cache htmlcov .coverage

clean: clean_tests
	rm -rf .eggs build dist src/ods_datasets_manager.egg-info

pre-commit:
