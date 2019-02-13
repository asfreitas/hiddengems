-- CitiesCities- MySQL Script generated by MySQL Workbench
-- Fri Feb  8 18:11:58 2019
-- CitiesModel: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

-- -----------------------------------------------------
-- Schema cs340_brassev
-- -----------------------------------------------------
USE `cs340_brassev` ;

-- -----------------------------------------------------
-- Table `cs340_brassev`.`Cities`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Cities` (
  `idCities` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `latitude` FLOAT NULL,
  `longitude` FLOAT NULL,
  `name` VARCHAR(45) NOT NULL,
  `state` VARCHAR(45) NULL,
  `country` VARCHAR(45) NULL,
  PRIMARY KEY (`idCities`),
  UNIQUE INDEX `idCities_UNIQUE` (`idCities` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cs340_brassev`.`Users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Users` (
  `idUsers` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `home_city` INT UNSIGNED NULL,
  `password` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idUsers`),
  UNIQUE INDEX `idUsers_UNIQUE` (`idUsers` ASC),
  INDEX `home_city_idx` (`home_city` ASC),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC),
  CONSTRAINT `home_city`
    FOREIGN KEY (`home_city`)
    REFERENCES `Cities` (`idCities`)
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cs340_brassev`.`Gems`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Gems` (
  `idGems` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `address` VARCHAR(45) NOT NULL,
  `type` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `description` MEDIUMTEXT NOT NULL,
  `created_by` INT UNSIGNED NULL,
  `location` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`idGems`),
  INDEX `created_by_idx` (`created_by` ASC),
  INDEX `location_idx` (`location` ASC),
  CONSTRAINT `created_by`
    FOREIGN KEY (`created_by`)
    REFERENCES `Users` (`idUsers`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `location`
    FOREIGN KEY (`location`)
    REFERENCES `Cities` (`idCities`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cs340_brassev`.`Reviews`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Reviews` (
  `idReviews` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `created` DATETIME NOT NULL,
  `contents` LONGTEXT NOT NULL,
  `written_by` INT UNSIGNED NOT NULL,
  `gem` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`idReviews`),
  INDEX `written_by_idx` (`written_by` ASC),
  INDEX `reviewed_gem_idx` (`gem` ASC),
  CONSTRAINT `written_by`
    FOREIGN KEY (`written_by`)
    REFERENCES `Users` (`idUsers`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `reviewed_gem`
    FOREIGN KEY (`gem`)
    REFERENCES `Gems` (`idGems`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cs340_brassev`.`Favorites`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Favorites` (
  `user` INT UNSIGNED NOT NULL,
  `gem` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`user`, `gem`),
  INDEX `gem_idx` (`gem` ASC),
  CONSTRAINT `user`
    FOREIGN KEY (`user`)
    REFERENCES `Users` (`idUsers`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `gem`
    FOREIGN KEY (`gem`)
    REFERENCES `Gems` (`idGems`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;
