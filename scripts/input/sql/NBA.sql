--
-- Create database
--
CREATE DATABASE IF NOT EXISTS nba_stats;
USE nba_stats;



--
-- Drop tables
-- turn off FK checks temporarily to eliminate drop order issues
--

SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS team, season, college, state_country, player, season_player, temp_player, temp_season_player;
SET FOREIGN_KEY_CHECKS=1;



--
-- Create Tables Team->
CREATE TABLE IF NOT EXISTS team (
	team_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	team_name VARCHAR(255) NULL,
	PRIMARY KEY (team_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;


LOAD DATA LOCAL INFILE './output/team_name.csv'
INTO TABLE team
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (team_name);
--


--
-- Create Tables Team->
CREATE TABLE IF NOT EXISTS season (
	season_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	season_year INTEGER NOT NULL UNIQUE,
	season_game INTEGER NULL,
	PRIMARY KEY (season_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/season.csv'
INTO TABLE season
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (season_year,season_game);
--


--
-- Create Tables Team->
CREATE TABLE IF NOT EXISTS college (
	college_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	college_name VARCHAR(255) NOT NULL,
	PRIMARY KEY (college_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/college.csv'
INTO TABLE college
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (college_name);
--


--
-- Create Tables State_Country->
CREATE TABLE IF NOT EXISTS state_country (
	state_country_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	state_country_name VARCHAR(255) NOT NULL,
	PRIMARY KEY (state_country_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/state.csv'
INTO TABLE state_country
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (state_country_name);
--




-- 
-- Create Temporary Table Player->
CREATE TABLE IF NOT EXISTS temp_player (
	player_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	player_name VARCHAR(255) NOT NULL,
	player_height REAL NULL,
	player_weight REAL NULL,
	player_birth_year REAL NULL,
	player_birth_state_name VARCHAR(255) NULL,
	player_college_name VARCHAR(255) NULL,
	PRIMARY KEY (player_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/player_info_trimmed.csv'
INTO TABLE temp_player
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (@dummy, player_name, player_height, player_weight, player_college_name, player_birth_year, @dummy, player_birth_state_name)


  SET player_name = IF(player_name = '', NULL, player_name),
	  player_height = IF(player_height = '', NULL, player_height),
      player_weight = IF(player_weight = '', NULL, player_weight),
      player_birth_year = IF(player_birth_year = '', NULL, player_birth_year),
      player_birth_state_name = IF(player_birth_state_name = '', NULL, player_birth_state_name),
      player_college_name = IF(player_college_name = '', NULL, player_college_name);
  
--



--
-- Create Table Player->
CREATE TABLE IF NOT EXISTS player (
	player_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	player_name VARCHAR(255) NOT NULL,
	player_height REAL NULL,
	player_weight REAL NULL,
	player_birth_year REAL NULL,
	player_birth_state_id INT NULL,
	player_college_id INT NULL,
	PRIMARY KEY (player_id),
	FOREIGN KEY (player_college_id) REFERENCES College(college_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (player_birth_state_id) REFERENCES State_Country(state_country_id)
    ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO player
  (
    player_name,
    player_height,
    player_weight,
    player_birth_year,
    player_birth_state_id,
    player_college_id
  )
SELECT tp.player_name, tp.player_height, tp.player_weight, tp.player_birth_year, sc.state_country_id, co.college_id
FROM temp_Player tp
LEFT JOIN College co
ON co.college_name = tp.player_college_name
LEFT JOIN State_Country sc
ON sc.state_country_name = tp.player_birth_state_name
WHERE IFNULL(co.college_name, 0) = IFNULL(tp.player_college_name, 0)
AND IFNULL(sc.state_country_name, 0) = IFNULL(tp.player_birth_state_name, 0)
ORDER BY tp.player_id;


-- ok for now --



--
-- Create Table Season_Player ->
CREATE TABLE IF NOT EXISTS temp_season_player (
	season_player_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	player_name VARCHAR(255) NOT NULL,
	team_name VARCHAR(255) NOT NULL,
	season_name VARCHAR(255) NOT NULL,
	player_age INTEGER,
	player_games INTEGER,
	player_minutes VARCHAR(10),
	player_PER VARCHAR(10),
	player_TS VARCHAR(10),
	player_OWS VARCHAR(10),
	player_DWS VARCHAR(10),
	player_WS VARCHAR(10),
	player_WS_per VARCHAR(10),
	player_FG VARCHAR(10),
	player_FGP VARCHAR(10),
	player_three_FG VARCHAR(10),
	player_three_FGP VARCHAR(10),
	player_TRB VARCHAR(10),
	player_AST VARCHAR(10),
	player_STL VARCHAR(10),
	player_BLK VARCHAR(10),
	player_TOV VARCHAR(10),
	player_PF VARCHAR(10),
	player_PTS VARCHAR(10),
	PRIMARY KEY(season_player_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/nba_info_trimmed.csv'
INTO TABLE temp_season_player
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (@dummy, season_name, player_name, @dummy, player_age, team_name, player_games, @dummy, player_minutes, player_PER, player_TS,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,player_OWS,player_DWS,player_WS,player_WS_per,@dummy,@dummy,@dummy,@dummy,@dummy,player_FG,@dummy,player_FGP,player_three_FG,@dummy,player_three_FGP,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,player_TRB,player_AST,player_STL,player_BLK,player_TOV,player_PF,player_PTS)

  SET player_age = IF(player_age = '', NULL, player_age),
	  player_games = IF(player_games = '', NULL, player_games),
      player_minutes = IF(player_minutes = '', NULL, player_minutes),
      player_TS = IF(player_TS = '', NULL, player_TS),
      player_OWS = IF(player_OWS = '', NULL, player_OWS),
      player_DWS = IF(player_DWS = '', NULL, player_DWS),
      player_WS = IF(player_WS = '', NULL, player_WS),
      player_WS_per = IF(player_WS_per = '', NULL, player_WS_per),
      player_FG = IF(player_FG = '', NULL, player_FG),
      player_FGP = IF(player_FGP = '', NULL, player_FGP),
      player_three_FG = IF(player_three_FG = '', NULL, player_three_FG),
      player_three_FGP = IF(player_three_FGP = '', NULL, player_three_FGP),
      player_TRB = IF(player_TRB = '', NULL, player_TRB),
      player_AST = IF(player_AST = '', NULL, player_AST),
      player_STL = IF(player_STL = '', NULL, player_STL),
      player_BLK = IF(player_BLK = '', NULL, player_BLK),
      player_TOV = IF(player_TOV = '', NULL, player_TOV),
      player_PF = IF(player_PF = '', NULL, player_PF),
      player_PTS = IF(player_PTS = '', NULL, player_PTS);

--


--
-- Create Table Player->
CREATE TABLE IF NOT EXISTS season_player (
	season_player_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	player_id INTEGER NOT NULL,
	team_id INTEGER NOT NULL,
	season_id INTEGER(255) NOT NULL,
	player_age INTEGER,
	player_games INTEGER,
	player_minutes INTEGER,
	player_PER DECIMAL(10,1),
	player_TS DECIMAL(10,3),
	player_OWS DECIMAL(10,1),
	player_DWS DECIMAL(10,1),
	player_WS DECIMAL(10,1),
	player_WS_per DECIMAL(10,3),
	player_FG INTEGER,
	player_FGP DECIMAL(10,3),
	player_three_FG DECIMAL(10),
	player_three_FGP DECIMAL(10,3),
	player_TRB INTEGER,
	player_AST INTEGER,
	player_STL INTEGER,
	player_BLK INTEGER,
	player_TOV INTEGER,
	player_PF INTEGER,
	player_PTS INTEGER,
	PRIMARY KEY(season_player_id),
	FOREIGN KEY (player_id) REFERENCES Player(player_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (team_id) REFERENCES Team(team_id)
    ON DELETE CASCADE ON UPDATE CASCADE,	
	FOREIGN KEY (season_id) REFERENCES Season(season_id)
    ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO season_player
  (
    season_player_id,
    player_id,
    team_id,
    season_id,
	player_age,
	player_games,
	player_minutes,
	player_PER,
	player_TS,
	player_OWS,
	player_DWS,
	player_WS,
	player_WS_per,
	player_FG,
	player_FGP,
	player_three_FG,
	player_three_FGP,
	player_TRB,
	player_AST,
	player_STL,
	player_BLK,
	player_TOV,
	player_PF,
	player_PTS
  )
SELECT sp.season_player_id, p.player_id, t.team_id, s.season_id, sp.player_age, sp.player_games, sp.player_minutes, sp.player_PER, sp.player_TS, sp.player_OWS, sp.player_DWS, sp.player_WS, sp.player_WS_per, sp.player_FG, sp.player_FGP, sp.player_three_FG, sp.player_three_FGP, sp.player_TRB, sp.player_AST, sp.player_STL, sp.player_BLK, sp.player_TOV, sp.player_PF, sp.player_PTS
FROM temp_season_player sp
LEFT JOIN Player p
ON p.player_name = sp.player_name
LEFT JOIN Season s
ON s.season_year = sp.season_name
LEFT JOIN Team t
ON t.team_name = sp.team_name
WHERE IFNULL(t.team_name, 0) = IFNULL(sp.team_name, 0)
AND IFNULL(s.season_year, 0) = IFNULL(sp.season_name, 0)
AND IFNULL(p.player_name, 0) = IFNULL(sp.player_name, 0)
ORDER BY sp.season_player_id;











DROP TABLE temp_player, temp_season_player;







