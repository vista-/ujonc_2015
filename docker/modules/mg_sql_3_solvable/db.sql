CREATE DATABASE test;
USE test;

# Main table
CREATE TABLE products(
    id int NOT NULL AUTO_INCREMENT,
    name varchar(100) DEFAULT NULL,
    description varchar(200) DEFAULT NULL,
    price int NOT NULL,
    PRIMARY KEY(id)
);
INSERT INTO products
    (name, description, price)
VALUES
    ('Kiwi', 'Green', 15),
    ('Apple', 'Yummy', 10),
    ('Water Mellon', 'Green', 30),
    ('Potato', 'For french fries', 40),
    ('Ananas', 'For pizza', 5),
    ('Secrets', 'are in an other table', 100);

# Secrets table
CREATE TABLE secrets(secret varchar(100));
INSERT INTO secrets (secret) VALUES ('BLACKLIST_TECHNOLOGY_FOR_THE_WIN');

COMMIT;
