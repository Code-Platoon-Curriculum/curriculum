-- DROP TABLE IF EXISTS students;

-- CREATE TABLE students(
--     student_id SERIAL PRIMARY KEY, -- UNIQUE, incrementing NOT repeating
--     student_name VARCHAR(100), -- type string, max chars 100
--     student_email VARCHAR(255) UNIQUE
-- );

-- INSERT INTO students(student_name, student_email) VALUES('james', 'james@james.com');
-- INSERT INTO students(student_name, student_email) VALUES('gary', 'james@james.com');

-- DROP TABLE IF EXISTS movies;

-- CREATE TABLE movies(
--     movie_id SERIAL PRIMARY KEY,
--     movie_name VARCHAR(255) UNIQUE CHECK(movie_name ~ '^[A-Z][a-z]*$'),
--     age_limit INT CHECK (age_limit IN (13, 15, 18)) -- age_limit BETWEEN 0 AND 18
--                                                     -- age_lmit >= 0 AND age_lmit <= 18
-- );

-- INSERT INTO movies(movie_name, age_limit) VALUES('PYTHON', 15);
-- INSERT INTO movies(movie_name, age_limit) VALUES('It', 18);

-- DROP TABLE IF EXISTS product;

-- CREATE TABLE product(
--     product_id SERIAL PRIMARY KEY,
--     product_name VARCHAR(100) UNIQUE NOT NULL,
--     quantity INT,
--     CHECK(quantity > 0)
-- );

-- INSERT INTO product(product_name, quantity) VALUES('grill cheese makers', 0);

DROP TABLE IF EXISTS games;

CREATE TABLE games(
    game_id SERIAL PRIMARY KEY,
    -- unique, regex, not null
    game_title VARCHAR(50) UNIQUE NOT NULL 
        CHECK(game_title ~ '^[A-Za-z09 _\-:''\\]'),
    -- greater or equal to 0 - 100 not null default 0
    quantity INT NOT NULL DEFAULT 0,
    -- greater or equal to 0 less  than or equal to 69.99
    price DECIMAL(4,2) DEFAULT 10,
    CHECK(quantity BETWEEN 0 AND 50),
    CHECK(price BETWEEN 0 AND 69.99)
);

\COPY games FROM '../data/game.csv' WITH CSV HEADER;