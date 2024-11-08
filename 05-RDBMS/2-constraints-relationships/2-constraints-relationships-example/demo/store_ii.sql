DROP TABLE IF EXISTS games;

CREATE TABLE games(
    game_id SERIAL PRIMARY KEY,
    game_title VARCHAR(50) NOT NULL UNIQUE,
    quantity INT,
    price DECIMAL(4,2)
);


\COPY games FROM '../data/game.csv' WITH CSV HEADER;

SELECT * FROM games_game_id_seq;
SELECT setval('games_game_id_seq', (SELECT MAX(game_id) FROM games));
SELECT * FROM games_game_id_seq;

INSERT INTO games(game_title, quantity, price) VALUES('Juans Game', 100, 10.99);
INSERT INTO games(game_title, quantity, price) VALUES('Garys Game', 10, 90.00);

ALTER TABLE games
DROP COLUMN is_fun;