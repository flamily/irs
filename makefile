venv:
	pipenv shell || true

run-db: venv
	docker run --rm -p 5432:5432 irs_db

stop-db: venv
	echo "Find docker container by typing: docker ps -a" && echo "Please kill the container with: docker rm -f [FIRST_TWO_DIGITS]"

install: venv
	pip install pipenv && pipenv install --ignore-pipfile

install-cognitiveface:
	git clone https://github.com/Microsoft/Cognitive-Face-Python.git
	cd Cognitive-Face-Python && python setup.py install

tests: venv
	pytest

lint: venv
	find . -iname "*.py" | xargs pylint

clean: venv
	find . -name '*.pyc' -delete





