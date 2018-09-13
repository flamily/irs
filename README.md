# irs

[![Build Status](https://travis-ci.com/flamily/irs.svg?token=VUn8qmicz1VXeQANksbc&branch=master)](https://travis-ci.com/flamily/irs)


## Database

Instructions for local machine database development. The following assumes that you:

1. Are running on a linux based machine.
2. Installed postgresql and during this process, the default postgres user has been created.
3. The postgresql localhost server is running.
4. You have created a database called `irs`.

### Creation
After creating a new database called irs, run this command to generate schema:
```
$ sudo -u postgres psql irs < db/schema.sql
```
This structure will be loaded into the default `public` schema.

### Nuking
To start from scratch, make sure you are in the psql cmd prompt and run:
```
# DROP SCHEMA public CASCADE;
# CREATE SCHEMA public;
```
