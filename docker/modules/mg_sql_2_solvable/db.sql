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
    ('Kiwi', 'Yellow', 15),
    ('Apple', 'Brown', 10),
    ('Water Mellon', 'Grey', 30),
    ('Potato', 'Small', 40),
    ('Ananas', 'Green', 5),
    ('Secrets', 'are in an other table', 100);

# Secrets table
CREATE TABLE secrets(secret varchar(100));
INSERT INTO secrets (secret) VALUES ('OUR_PHP_USES_ROT13_FOR_MAXIMUM_SECURITY');

COMMIT;
