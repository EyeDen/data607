-- movies.sql

DROP TABLE IF EXISTS movies;

CREATE TABLE movies
(
	id int NOT NULL,
	sex char(1) NOT NULL,
	Thor_Ragnarok int NOT NULL,
	Rogue_One int NOT NULL,
	Last_Jedi int NOT NULL,
	Blade_Runner_2049 int NOT NULL,
	Dunkirk int NOT NULL,
	Baby_Driver int NOT NULL
);

SELECT * FROM movies;

LOAD DATA LOCAL INFILE 'C:/data/movies.csv'
INTO TABLE movies
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(id, sex, Thor_Ragnarok, Rogue_One, Last_Jedi, Blade_Runner_2049, Dunkirk, Baby_Driver);

SELECT COUNT(*) FROM movies;