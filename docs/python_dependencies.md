# Manually installing python dependencies with `pipenv`

Pipenv, serves to simplify the management of dependencies in Python-based projects. It brings together Pip, Pipfile and Virtualenv to provide a straightforward and powerful approach to package management. To get started, install `pipenv` using your pip manager for python3:
```
$ pip install pipenv
```
Then, to install the specific dependencies for this project, navigate to the project directory and run:
```
user@foo: ~ $ cd irs
user@foo: ~/irs $ pipenv install --ignore-pipfile
... pipenv does it's thing ...
```
You are now ready to tango! The easiest way to see if it worked is to drop into a virtualenv and run the test suite:
```
user@foo: ~/irs $ pipenv shell
(irs-0Z00RQNN) user@foo: ~/irs $ pytest
... testing ...
(irs-0Z00RQNN) user@foo: ~/irs $ exit
user@foo: ~/irs $
```
For you to be able to run any of the applications, everything must occur within a `pipenv shell`, or,  commands must be prefaced with `pipenv run`:
```
$ pipenv run python some_app.py
```
