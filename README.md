# optimus-type.api-server

[![Build Status](https://travis-ci.org/hesoyam11/optimus-time.api-server.svg?branch=master)](https://travis-ci.org/hesoyam11/optimus-type.api-server)
[![codecov](https://codecov.io/gh/hesoyam11/optimus-type.api-server/branch/master/graph/badge.svg)](https://codecov.io/gh/hesoyam11/optimus-type.api-server)

## Setup development environment

1. Create `.env` file and set the following variables in it:
    * `DATABASE_NAME`
    * `DATABASE_USER`
    * `DATABASE_PASSWORD`
    * `DATABASE_HOST`
    * `DATABASE_PORT`
1. `sudo -u postgres psql`
1. Run the following queries against your PostgreSQL database:
    ```sql
    CREATE DATABASE <DATABASE_NAME>;
    CREATE USER <DATABASE_USER> WITH PASSWORD '<DATABASE_PASSWORD>';
    
    ALTER ROLE <DATABASE_USER> SET client_encoding TO 'utf8';
    ALTER ROLE <DATABASE_USER> SET default_transaction_isolation TO 'read committed';
    ALTER ROLE <DATABASE_USER> SET timezone TO 'UTC';
    
    GRANT ALL PRIVILIGES ON DATABASE <DATABASE_NAME> TO <DATABASE_USER>;
    ALTER USER <DATABASE_USER> CREATEDB;
    \q
    ```
1. `pipenv install --dev`
1. `pipenv run python manage.py migrate`
1. `pipenv run python manage.py runserver`

## Setup production environment

TODO: `CORS_ORIGIN_WHITELIST`