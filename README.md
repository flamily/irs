# irs

[![Build Status](https://travis-ci.com/flamily/irs.svg?token=VUn8qmicz1VXeQANksbc&branch=master)](https://travis-ci.com/flamily/irs)

## Automated Testing & Quality

There are a few testing processes which run on Travis CI for each commit. The idea is to maintain the quality of the system using automated processes. It's not supposed to make your life a misery, so raise an issue if it is getting in the way.

The Spice Must Flow!

With that in mind, these are the processes, what they are looking for and the intended goals:

### pytest

Running `pytest` in the root directory will run all the unit tests.

### Coverage

`Coverage` is a tool to enforce test coverage. Running `coverage run -m pytest` in the root will run all the tests, but also track which lines of code are executed. Subsequently running `coverage report` prints an overview of the test coverage. Travis CI uses additional flags to fail the build when any of the files have a coverage below 100%.

### pylint

`pylint` automagically tells everyone when your code is garbage- it even prints a helpful score!

However, there are some checks which are disabled:

* `C0111` Missing docstring: Not _everything_ needs a comment
*


## Database

Instructions for local machine database development. The following assumes that you:

1. Are running on a linux based machine.
2. Installed postgresql and during this process, the default postgres user has been created.
3. The postgresql localhost server is running.
4. You have created a database called `irs`.

### Creation
After creating a new database called irs, run this command from terminal to generate schema:
```
sudo -u postgres psql irs < db/schema.sql
```
This structure will be loaded into the default `public` schema. Developers may also want to load some test records to their database. They can do so with the `test.sql` script:

```
sudo -u postgres psql irs < db/test.sql
```

### Nuking
To start from scratch, run:
```
echo "DROP SCHEMA public CASCADE; CREATE SCHEMA public;" | sudo -u postgres psql irs
```
