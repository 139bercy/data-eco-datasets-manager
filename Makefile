clean_tests:
	rm -rf .pytest_cache htmlcov .coverage

clean: clean_tests
	rm -rf .eggs build dist ods_datasets_manager.egg-info

