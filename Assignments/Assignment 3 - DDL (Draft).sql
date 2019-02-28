-- -----------------------------------------------------
-- Sample Data
-- -----------------------------------------------------
-- Cities:
INSERT INTO `Cities` (`name`, `state`, `country`, `latitude`, `longitude`) VALUES ('Corvallis', 'Oregon', 'USA', 44.574702, -123.274775);
INSERT INTO `Cities` (`name`, `state`, `country`, `latitude`, `longitude`) VALUES ('Albany', 'Oregon', 'USA', 44.629426, -123.099454);
INSERT INTO `Cities` (`name`, `state`, `country`, `latitude`, `longitude`) VALUES ('Bend', 'Oregon', 'USA', 44.057642, -121.311386);
INSERT INTO `Cities` (`name`, `state`, `country`, `latitude`, `longitude`) VALUES ('Cairo', NULL, 'Egypt', 30.040465, 31.235888);

-- Users:
INSERT INTO `Users` (`username`, `home_city`, `password`) SELECT 'love', `idCities`, 'butterflies' FROM `Cities` WHERE `name` = 'Albany';
INSERT INTO `Users` (`username`, `home_city`, `password`) SELECT 'joy', `idCities`, 'goodray55' FROM `Cities` WHERE `name` = 'Cairo';
INSERT INTO `Users` (`username`, `home_city`, `password`) SELECT 'peace', `idCities`, '!voryIvory39' FROM `Cities` WHERE `name` = 'Corvallis';
INSERT INTO `Users` (`username`, `home_city`, `password`) SELECT 'patience', `idCities`, 'sweetBe@n34' FROM `Cities` WHERE `name` = 'Cairo';
INSERT INTO `Users` (`username`, `home_city`, `password`) VALUES ('kindness', NULL, 'fir$tMind50');
INSERT INTO `Users` (`username`, `home_city`, `password`) VALUES ('goodness', NULL, 'password12345');
INSERT INTO `Users` (`username`, `home_city`, `password`) VALUES ('faithfullness', NULL, 'smartCir(le52');
INSERT INTO `Users` (`username`, `home_city`, `password`) VALUES ('gentleness', NULL, 'qwerty555');
INSERT INTO `Users` (`username`, `home_city`, `password`) VALUES ('self-control', NULL, 'busySt!ck72');

-- Gems:
INSERT INTO `Gems` (`address`, `type`, `name`, `description`, `created_by`, `location`) 
	SELECT '100 SW 2nd St', 'Tavern', 'Squirrel\'s Tavern', '"A learning center in downtown Corvallis"', `idUsers`, `idCities` FROM `Users` INNER JOIN `Cities` WHERE 
    `username` = 'love' AND `Cities`.`name` = 'Corvallis';
INSERT INTO `Gems` (`address`, `type`, `name`, `description`, `created_by`, `location`) 
	SELECT '1425 NW Monroe Ave', 'Resteraunt', 'Tian Fu Noodle', '#1 agreed upon fact in Corvallis is that this is the #1 restaurant Vegetarian noodles are delicious!', `idUsers`, `idCities` FROM `Users` INNER JOIN `Cities` WHERE 
    `username` = 'goodness' AND `Cities`.`name` = 'Corvallis';
INSERT INTO `Gems` (`address`, `type`, `name`, `description`, `created_by`, `location`) 
	SELECT '116 NW 3rd St', 'Donut Shop', 'Benny\'s Donuts', 'Little Donuts with big flavors', `idUsers`, `idCities` FROM `Users` INNER JOIN `Cities` WHERE 
    `username` = 'self-control' AND `Cities`.`name` = 'Corvallis';
INSERT INTO `Gems` (`address`, `type`, `name`, `description`, `created_by`, `location`) 
	SELECT '500 SW 2nd St', 'Coffee Shop', 'Allan Bros - Beanery', 'Good Coffee', `idUsers`, `idCities` FROM `Users` INNER JOIN `Cities` WHERE 
    `username` = 'joy' AND `Cities`.`name` = 'Corvallis';
INSERT INTO `Gems` (`address`, `type`, `name`, `description`, `created_by`, `location`) 
	SELECT '1556, 2215 NW 9th St', 'Coffee Shop', 'Coffee Culture', 'Coffee Culture Annex', NULL, `idCities` FROM `Cities` WHERE 
    `Cities`.`name` = 'Corvallis';
    
-- Reviews:
INSERT INTO `Reviews` (`created`, `contents`, `written_by`, `gem`) 
	SELECT CURRENT_TIMESTAMP, 'This place was great.', `idUsers`, `idGems` FROM `Users` INNER JOIN `Gems` WHERE 
    `username` = 'gentleness' AND `Gems`.`name` = 'Coffee Culture';
INSERT INTO `Reviews` (`created`, `contents`, `written_by`, `gem`) 
	SELECT CURRENT_TIMESTAMP, 'I love Benny\'s!', `idUsers`, `idGems` FROM `Users` INNER JOIN `Gems` WHERE 
    `username` = 'love' AND `Gems`.`name` = 'Benny\'s Donuts';
INSERT INTO `Reviews` (`created`, `contents`, `written_by`, `gem`) 
	SELECT CURRENT_TIMESTAMP, 'Set youreself a limit before you walk in the door.', `idUsers`, `idGems` FROM `Users` INNER JOIN `Gems` WHERE 
    `username` = 'self-control' AND `Gems`.`name` = 'Benny\'s Donuts';
    
-- Favorites:
INSERT INTO `Favorites` (`user`, `gem`) SELECT `idUsers`, `idGems` FROM `Users` INNER JOIN `Gems` WHERE 
    `username` = 'love' AND `Gems`.`name` = 'Squirrel\'s Tavern';
INSERT INTO `Favorites` (`user`, `gem`) SELECT `idUsers`, `idGems` FROM `Users` INNER JOIN `Gems` WHERE 
    `username` = 'love' AND `Gems`.`name` = 'Tian Fu Noodle';
INSERT INTO `Favorites` (`user`, `gem`) SELECT `idUsers`, `idGems` FROM `Users` INNER JOIN `Gems` WHERE 
    `username` = 'love' AND `Gems`.`name` = 'Benny\'s Donuts';
INSERT INTO `Favorites` (`user`, `gem`) SELECT `idUsers`, `idGems` FROM `Users` INNER JOIN `Gems` WHERE 
    `username` = 'love' AND `Gems`.`name` = 'Allan Bros - Beanery';
INSERT INTO `Favorites` (`user`, `gem`) SELECT `idUsers`, `idGems` FROM `Users` INNER JOIN `Gems` WHERE 
    `username` = 'love' AND `Gems`.`name` = 'Coffee Culture';
INSERT INTO `Favorites` (`user`, `gem`) SELECT `idUsers`, `idGems` FROM `Users` INNER JOIN `Gems` WHERE 
    `username` = 'peace' AND `Gems`.`name` = 'Coffee Culture';
INSERT INTO `Favorites` (`user`, `gem`) SELECT `idUsers`, `idGems` FROM `Users` INNER JOIN `Gems` WHERE 
    `username` = 'faithfullness' AND `Gems`.`name` = 'Benny\'s Donuts';
