# create database and load schema
if psql -lqt | cut -d \| -f 1 | grep -qw irs; then
  # just humour me and let's start with a clean slate yeah? Cool.
  echo IRS database already exists. Dropping table IRS.
  sudo -u postgres psql -c 'DROP DATABASE irs'
fi
sudo -u postgres psql -c 'CREATE DATABASE irs OWNER postgres'
echo Loading schema...
sudo -u postgres psql irs < db/schema.sql
echo -e '\n' Database and schema created successfully! '\n'
