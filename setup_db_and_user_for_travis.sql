CREATE DATABASE optimus_type;
CREATE USER optimus_type_admin WITH PASSWORD 'optimus_type';
ALTER ROLE optimus_type_admin SET client_encoding TO 'utf8';
ALTER ROLE optimus_type_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE optimus_type_admin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE optimus_type TO optimus_type_admin;
ALTER USER optimus_type_admin CREATEDB;
