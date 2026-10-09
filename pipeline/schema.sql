-- This file should contain all code required to create & seed database tables.

DROP DATABASE IF EXISTS museum;
CREATE DATABASE museum;

DROP TABLE IF EXISTS floors CASCADE;
DROP TABLE IF EXISTS departments CASCADE;
DROP TABLE IF EXISTS request_types CASCADE;
DROP TABLE IF EXISTS rating_types CASCADE;
DROP TABLE IF EXISTS exhibitions CASCADE;
DROP TABLE IF EXISTS requests CASCADE;
DROP TABLE IF EXISTS ratings CASCADE;

\c museum;

SET datestyle = 'ISO, DMY';

CREATE TABLE floors (
    floor_id INT GENERATED ALWAYS AS IDENTITY,
    floor_name TEXT NOT NULL,
    PRIMARY KEY (floor_id)
);

INSERT INTO floors (floor_name)
VALUES
    ('Vault'),
    ('1'),
    ('2'),
    ('3');


CREATE TABLE departments (
    department_id INT GENERATED ALWAYS AS IDENTITY,
    department_name TEXT NOT NULL,
    PRIMARY KEY (department_id)
);


INSERT INTO departments (department_name)
VALUES
    ('Entomology'),
    ('Geology'),
    ('Paleontology'),
    ('Zoology'),
    ('Ecology');

CREATE TABLE request_types (
    request_type_id INT GENERATED ALWAYS AS IDENTITY,
    request_value INT UNIQUE NOT NULL,
    request_name TEXT NOT NULL,
    PRIMARY KEY (request_type_id)
);

INSERT INTO request_types (request_value, request_name)
VALUES
    (0, 'Assistance'),
    (1, 'Emergency');

CREATE TABLE rating_types(
    rating_id INT GENERATED ALWAYS AS IDENTITY,
    rating_value INT UNIQUE NOT NULL,
    rating_name TEXT NOT NULL,
    PRIMARY KEY (rating_id)
);

INSERT INTO rating_types (rating_value, rating_name)
VALUES
    (0, 'Terrible'),
    (1, 'Bad'),
    (2, 'Neutral'),
    (3, 'Good'),
    (4, 'Amazing');

CREATE TABLE exhibitions (
    exhibition_id INT GENERATED ALWAYS AS IDENTITY,
    department_id INT NOT NULL,
    floor_id INT NOT NULL,
    exhibition_name TEXT UNIQUE NOT NULL,
    start_date DATE NOT NULL,
    PRIMARY KEY (exhibition_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (floor_id) REFERENCES floors(floor_id)
);


CREATE TABLE requests(
    request_id INT GENERATED ALWAYS AS IDENTITY,
    exhibition_id INT NOT NULL,
    request_value INT NOT NULL,
    time_at TIMESTAMP NOT NULL,
    PRIMARY KEY (request_id),
    FOREIGN KEY (exhibition_id) REFERENCES exhibitions(exhibition_id),
    FOREIGN KEY (request_value) REFERENCES request_types(request_value)
);


CREATE TABLE ratings(
    rating_id INT GENERATED ALWAYS AS IDENTITY,
    exhibition_id INT NOT NULL,
    rating_value INT NOT NULL,
    time_at TIMESTAMP NOT NULL,
    PRIMARY KEY (rating_id),
    FOREIGN KEY (exhibition_id) REFERENCES exhibitions(exhibition_id),
    FOREIGN KEY (rating_value) REFERENCES rating_types(rating_value)
);
