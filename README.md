# irs

[![Build Status](https://travis-ci.com/flamily/irs.svg?token=VUn8qmicz1VXeQANksbc&branch=master)](https://travis-ci.com/flamily/irs)

## Development environment

Please make sure:
1. Installed postgresql and during this process, the default postgres user has been created.
2. The postgresql localhost server is running.

### Viewing flask templates

`routes.py` handles all the template rendering. To view the templates in your browser, you can run a local flask server.
```
  FLASK_APP=routes.py flask run
```
Then you can view it on `http://127.0.0.1:5000/`

### Database

_Note: the automated setup will create a db for you as postgres user and also load the schema, pipenv and requirements as well as the pre-commit hooks_

To run the automated setup, please ensure that you are at the root irs folder (run `cd irs` to double check) then run the script:
```
./setup.sh
```
It might prompt you for a password as it runs some commands as a sudo user. Just type in your password.

Viola! You're good to go.

### Manual Setup

1. For the database, you can either run the [docker container](#Docker) OR you can create the [create the irs database](wiki/Database) and [load the schema](wiki/Database#loadtheschema). _We recommend running the docker container._

2. Install [pipenv](wiki/Managing-Python-Dependencies) to manage depencies.
3. Intall [pre-commit](wiki/Pre-commit-hook) to run code checks on commit.

## Docker

For most developers, you shouldn't worry about fiddling with databases. In terms of automated unit testing however, you will need an instance of postgres running. As such, use `docker` to handle all the setup for you:
```
    $ docker run --rm -p 5432:5432 postgres
```

## Using Pipenv

Pipenv, serves to simplify the management of dependencies in Python-based projects. It brings together Pip, Pipfile and Virtualenv to provide a straightforward and powerful approach to package management.

For you to be able to run any of the applications, everything must occur within a `pipenv shell`, or commands must be prefaced with `pipenv run`:
```
$ pipenv run python some_app.py
```

## Automated Testing & Quality

There are a few testing processes which run on Travis CI for each commit. The idea is to maintain the quality of the system using automated processes. It's not supposed to make your life a misery, so raise an issue if it is getting in the way- The spice must flow!

With that in mind, these are the processes, what they are looking for and the intended goals:

### Pre-commit Hooks

The pre-commit hook will run when you make a commit. This includes flake8, pylint and other code style checks. When it can, pre-commit will correct those files for you. To find out more about the specific pre-commit checks, you can find it in the [wiki](wiki/Pre-commit-hook).

*Note: You will need to re-add any files that pre-commit fixes up for you. If there weren't any and it passed everything then you may commit what your original staged files*

### Testing

Running `pytest` in the root directory will run all the unit tests. Pytest is verifying for implementation correctness and to make sure there are no regressions. The idea is to ensure that the code is exercised and we know that it works.
```
$ pytest
```
Before running `pytest`, spin up a development database using [docker](#Docker).


### Coverage

`Coverage` is a tool to enforce test coverage. Running `coverage run -m pytest` in the root will run all the tests, but also track which lines of code are executed. Subsequently running `coverage report` prints an overview of the test coverage. Travis CI uses additional flags to fail the build when any of the files have a coverage below 100%. The goal is to exercise all of the code, have no dead bits and know for sure that all of it works.
