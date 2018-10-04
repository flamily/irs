# Pre-commit Checks

## Manually installing pre-commit git hooks

`pre-commit` does some syntax and code quality checks for code style, flake8 and pylint. When it can, pre-commit will correct those files for you.

To install:
```
sudo -H pip install pre-commit --user --no-warn-script-location
pre-commit install -f --install-hooks
```

To use, simply run:
```
$ git add {files that were modified by pre-commit}
$ git commit -m "happy days"
... checks happen ...
```
If it's a pylint error etc. fix up the files ...
```
$ git add [changes to files it identified as non-compliant]
$ git commit -m "happy days"
$ git push
```

*Note: You will need to re-add any files that pre-commit fixes up for you. If there weren't any and it
passed everything then you may commit what your original staged files*

## Pylint

`pylint` automagically tells everyone when your code is garbage- it even prints a helpful score! Automatic checks against best practices will keep the code clean and neat. However, there are some checks which are disabled:

* `C0111` Missing docstring: Not _everything_ needs a comment

his is automatically run as part of the pre-commit githook but if you would like to run it manually, simple execute:
```
find . -iname "*.py" | xargs pylint
```
The command ollowing will find all python files and run the linter over them.
