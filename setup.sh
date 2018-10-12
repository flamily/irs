#!/bin/bash

set -e

# set the correct path
export PATH="$PATH:$(python3 -m site --user-base)/bin"

# install pipenv
sudo -H pip3 install -U pipenv
pipenv install --ignore-pipfile

# install pre-commit using pip. Can't be installed with pipenv, it throws errors :(
echo -e '\n'
sudo -H pip install pre-commit --user --no-warn-script-location

# symlink hooks
pre-commit install -f --install-hooks
echo -e '\n' Success! Dev away you little potato gems... '\n'
