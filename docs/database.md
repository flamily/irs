# Database

Instructions for to manually create your local machine database development. The following assumes that you:

1. Are running on a linux based machine.
2. Installed postgresql and during this process, the default postgres user has been created.
3. The postgresql localhost server is running.
4. You have created a database called `irs`.

### Load the Schema
After creating a new database called irs, run this command from terminal to generate schema:
```
sudo -u postgres psql irs < db/schema.sql
```
This structure will be loaded into the default `public` schema.
Developers may also want to load some test records to their database.
They can do so with the `test.sql` script:

```
sudo -u postgres psql irs < db/test.sql
```

### Nuking
To start from scratch, run:
```
echo "DROP SCHEMA public CASCADE; CREATE SCHEMA public;" | sudo -u postgres psql irs
```
