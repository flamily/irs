# irs

[![Build Status](https://travis-ci.com/flamily/irs.svg?token=VUn8qmicz1VXeQANksbc&branch=master)](https://travis-ci.com/flamily/irs)

## Setup development environment
### Installing python dependencies with `pipenv`

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

### Database

Instructions for local machine database development. The following assumes that you:

1. Are running on a linux based machine.
2. Installed postgresql and during this process, the default postgres user has been created.
3. The postgresql localhost server is running.
4. You have created a database called `irs`.

#### Creation
After creating a new database called irs, run this command from terminal to generate schema:
```
$ sudo -u postgres psql irs < db/schema.sql
```
This structure will be loaded into the default `public` schema. Developers may also want to load some test records to their database. They can do so with the `test.sql` script:

```
$ sudo -u postgres psql irs < db/test.sql
```

#### Nuking
To start from scratch, run:
```
$ echo "DROP SCHEMA public CASCADE; CREATE SCHEMA public;" | sudo -u postgres psql irs
```


## Automated Testing & Quality

There are a few testing processes which run on Travis CI for each commit. The idea is to maintain the quality of the system using automated processes. It's not supposed to make your life a misery, so raise an issue if it is getting in the way- The spice must flow!

With that in mind, these are the processes, what they are looking for and the intended goals:

### Pre-commit Checks
Before doing your commits, git add your changed files and run `pre-commit` to do some syntax and code quality
checks. When it can, pre-commit will correct those files for you.

To use, simply run:
```
$ git add {files you want to commit}
$ pre-commit
... some stuff happens ...
$ git add {files that were modified by pre-commit}
$ git commit -m "happy days"
$ git push
```

*Note: You will need to re-add any files that pre-commit fixes up for you. If there weren't any and it
passed everything then you may commit what your original staged files*

### pytest

Running `pytest` in the root directory will run all the unit tests. Pytest is verifying for implementation correctness and to make sure there are no regressions. The idea is to ensure that the code is exercised and we know that it works.

### Coverage

`Coverage` is a tool to enforce test coverage. Running `coverage run -m pytest` in the root will run all the tests, but also track which lines of code are executed. Subsequently running `coverage report` prints an overview of the test coverage. Travis CI uses additional flags to fail the build when any of the files have a coverage below 100%. The goal is to exercise all of the code, have no dead bits and know for sure that all of it works.

### pylint

`pylint` automagically tells everyone when your code is garbage- it even prints a helpful score! Automatic checks against best practices will keep the code clean and neat. However, there are some checks which are disabled:

* `C0111` Missing docstring: Not _everything_ needs a comment

Running the following will find all python files and run the linter over them:
```
find . -iname "*.py" | xargs pylint
```
