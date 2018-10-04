#!/bin/bash

set -e

# set the correct path
export PATH="$PATH:$(python3 -m site --user-base)/bin"

# install pipenv
sudo -H pip install -U pipenv
pipenv install --ignore-pipfile

# create database and load schema
if psql -lqt | cut -d \| -f 1 | grep -qw irs; then
  # just humour me and let's start with a clean slate yeah? Cool.
  echo IRS database already exists. Dropping table IRS.
  sudo -u postgres psql -c 'DROP DATABASE irs'
fi
sudo -u postgres psql -c 'CREATE DATABASE irs OWNER postgres'
echo Loading schema...
sudo -u postgres psql irs < db/schema.sql
sudo -u postgres psql irs < db/test.sql

# install pre-commit using pip. This is something that was lost from the requirements.txt
# when shifting over to pipenv so let's make sure it's installed.
echo -en '\n'
sudo -H pip install pre-commit --user --no-warn-script-location
# symlink hooks
pre-commit install -f --install-hooks

echo -e Success! Dev away you little potato gems... '\n'
