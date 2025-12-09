CREATE DATABASE portal_juegos;
CREATE USER portal_user WITH PASSWORD 'portal_password';
GRANT ALL PRIVILEGES ON DATABASE portal_juegos TO portal_user;

\c portal_juegos;
GRANT ALL ON SCHEMA public TO portal_user;