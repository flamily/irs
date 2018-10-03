# irs

[![Build Status](https://travis-ci.com/flamily/irs.svg?token=VUn8qmicz1VXeQANksbc&branch=master)](https://travis-ci.com/flamily/irs)


## Seup development environment
### Installing python dependencies with `pipenv`

Pipenv, serves to simplify the management of dependencies in Python-based projects. It brings together Pip, Pipfile and Virtualenv to provide a straightforward and powerful approach to package management. To get started, install `pipenv` using your pip manager for python3:
```
$ pip install pipenv
```
Then, to install the specific dependencies for this project, navigate to the project directory and run:
```
user@foo: ~ $ cd irs
user@foo: ~/irs $ pipenv install
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


## Code Quality
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
