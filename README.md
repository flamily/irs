# irs

[![Build Status](https://travis-ci.com/flamily/irs.svg?token=VUn8qmicz1VXeQANksbc&branch=master)](https://travis-ci.com/flamily/irs)

## Development environment

Please make sure:
1. You're running a linux based machine.
2. Installed postgresql and during this process, the default postgres user has been created.
3. The postgresql localhost server is running.

### Automated Setup

_Note: the automated setup will create a db for you as postgres user and also load the schema, install requirements pipenv and requirems as well as the pre-commit hooks_

To run the automated setup, please ensure that you are at the root irs folder:
```
cd irs
```
then run the script:
```
./setup.sh
```
It might prompt you for a password as it runs some commands as a sudo user. Just type in your password.

Viola! You're good to go.

### Manual Setup

For manual setup:

1. Create the [irs database](docs/database.md#database) and load the [schema](docs/database#loadtheschema).
2. Install [pipenv](docs/python_dependencies#pipenv) to manage depencies.
3. Intall [pre-commit](docs/pre_commit) to run code checks on commit.

## Using Pipenv

Pipenv, serves to simplify the management of dependencies in Python-based projects. It brings together Pip, Pipfile and Virtualenv to provide a straightforward and powerful approach to package management.

For you to be able to run any of the applications, everything must occur within a `pipenv shell`, or commands must be prefaced with `pipenv run`:
```
$ pipenv run python some_app.py
```

## Automated Testing & Quality

There are a few testing processes which run on Travis CI for each commit. The idea is to maintain the quality of the system using automated processes. It's not supposed to make your life a misery, so raise an issue if it is getting in the way- The spice must flow!

With that in mind, these are the processes, what they are looking for and the intended goals:

### Pre-commit Checks
#### 1. Pre-commit hooks
The pre-commit checks will run when you make a commit. This includes flake8, pylint and other code style checks. When it can, pre-commit will correct those files for you. To find out more about the specific pre-commit checks, head over to [pre-commit](docs/pre_commit.md).

*Note: You will need to re-add any files that pre-commit fixes up for you. If there weren't any and it passed everything then you may commit what your original staged files*

### pytest

Running `pytest` in the root directory will run all the unit tests. Pytest is verifying for implementation correctness and to make sure there are no regressions. The idea is to ensure that the code is exercised and we know that it works.

### Coverage

`Coverage` is a tool to enforce test coverage. Running `coverage run -m pytest` in the root will run all the tests, but also track which lines of code are executed. Subsequently running `coverage report` prints an overview of the test coverage. Travis CI uses additional flags to fail the build when any of the files have a coverage below 100%. The goal is to exercise all of the code, have no dead bits and know for sure that all of it works.
