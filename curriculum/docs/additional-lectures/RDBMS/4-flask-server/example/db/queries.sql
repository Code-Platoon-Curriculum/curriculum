-- SELECT engine_name FROM gaming_engine;

-- SELECT SUM(quantity) AS total_game_inventory FROM game;

-- SELECT game_title AS title FROM game WHERE price > 30;

-- SELECT game_title AS title, quantity FROM game WHERE quantity < 20;

-- SELECT COUNT(*) FROM genre_game;

-- SELECT action_figure_title AS figure_title 
-- FROM action_figure 
-- WHERE price BETWEEN 20 AND 50;

-- SELECT poster_title, price
-- FROM poster
-- WHERE quantity BETWEEN 15 AND 30;

-- SELECT employee_name AS name, position
-- FROM employee
-- WHERE salary > 40000;

-- SELECT COUNT(*) FROM social_security;

-- SELECT start_time AS start, end_time AS end
-- FROM shifts;

-- SELECT e.employee_name AS name, e.salary AS salary, shifts.start_time
-- FROM employee e
-- JOIN shifts ON e.id = shifts.employee_id;

-- EXPLAIN ANALYZE SELECT COUNT(*)
-- FROM employee
-- WHERE employee_name ILIKE '%M%';

-- SELECT * FROM action_figure WHERE quantity < 15;

-- SELECT game_title AS title FROM game WHERE game_title LIKE '%Warzone%';

-- SELECT COUNT(*) FROM genre;

-- SELECT action_figure_title, quantity
-- FROM action_figure
-- WHERE price > 27;

-- SELECT employee_name AS name 
-- FROM employee
-- WHERE position = 'IT Specialist';

-- SELECT SUM(g.quantity) + SUM(af.quantity)+ SUM(p.quantity) AS total_quantity
-- FROM game g
-- FULL JOIN action_figure af ON g.game_id = af.id
-- FULL JOIN poster p ON af.id = p.id;

SELECT e.employee_name AS name, e.position
FROM employee e
JOIN shifts ON shifts.employee_id = e.id
WHERE shifts.start_time < '2024-03-07 13:00:00';
