CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'replicator_password';
SELECT pg_create_physical_replication_slot('replication_slot');
\c bot_database;
CREATE TABLE email_addresses (
    email_id SERIAL,
    address VARCHAR(255)
);
CREATE TABLE phone_numbers (
    phone_id SERIAL,
    number VARCHAR(18)
);

INSERT INTO email_addresses (address) VALUES 
('gorbanalex2002@gmail.com'),
('positive-start@yandex.ru');

INSERT INTO phone_numbers (number) VALUES 
('+7(777)777-55-55'),
('89998883322');