cov:
	coverage run -m pytest
	coverage html

test:
	ENV=test pytest tests -s
