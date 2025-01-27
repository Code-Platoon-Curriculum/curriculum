-- Drop the table if it exists
DROP TABLE IF EXISTS game;

-- Create Game Table
CREATE TABLE game (
    game_id INT PRIMARY KEY,
    game_title VARCHAR(255) UNIQUE NOT NULL CHECK (game_title ~ '^[A-Za-z0-9 _\-:''\\]+$'),
    quantity INT NOT NULL CHECK(quantity > 0 AND quantity < 51),
    price DECIMAL(5, 2) NOT NULL CHECK(price > 10 AND price < 60)
);


-- Insert Sample Data into Game Table
\COPY game FROM './data/game.csv' WITH CSV HEADER;


DROP TABLE IF EXISTS action_figure;

CREATE TABLE action_figure (
    id INT PRIMARY KEY,
    action_figure_title VARCHAR UNIQUE NOT NULL CHECK (action_figure_title ~ '^[A-Za-z0-9 _-]+$'),
    quantity INT NOT NULL CHECK(quantity > 0 AND quantity < 31),
    price DECIMAL(5,2) NOT NULL CHECK(price > 10 AND price < 100.01)
);

\COPY action_figure FROM './data/action_figure.csv' WITH CSV HEADER;

DROP TABLE IF EXISTS employee;

-- MAX SALARY AN HOUR IS 31.25 AND MIN IS 16.66
CREATE TABLE employee (
    id INT PRIMARY KEY,
    employee_name VARCHAR NOT NULL CHECK (employee_name ~ '^[A-Za-z ]+$'),
    position VARCHAR NOT NULL CHECK (position IN (
        'Sales Associate',
        'Store Manager',
        'Inventory Clerk',
        'Customer Service Representative',
        'IT Specialist',
        'Marketing Coordinator',
        'Assistant Manager',
        'Finance Analyst',
        'Security Officer',
        'HR Coordinator'
    )),
    salary DECIMAL(7,2) NOT NULL CHECK (salary > 31987.19 AND salary < 60000.01)
);

\COPY employee FROM './data/employee.csv' WITH CSV HEADER;

DROP TABLE IF EXISTS poster;

CREATE TABLE poster (
    id SERIAL PRIMARY KEY,
    poster_title VARCHAR UNIQUE NOT NULL CHECK (poster_title ~ '^[A-Za-z0-9 _-]+$'),
    quantity INT NOT NULL CHECK (quantity > 0 AND quantity < 31),
    price DECIMAL(4,2) NOT NULL CHECK (price <= 20.00 AND price > 6)
);


\COPY poster FROM './data/poster.csv' WITH CSV HEADER;