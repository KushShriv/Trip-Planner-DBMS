CREATE SCHEMA `trip_planner` ;

CREATE TABLE `trip_planner`.`customer` (
  `Customer ID` INT NOT NULL AUTO_INCREMENT,
  `Customer Name` VARCHAR(45) NULL,
  `Phone Number` VARCHAR(45) NULL,
  `Email` VARCHAR(45) NULL,
  `Password` VARCHAR(45) NULL,
  PRIMARY KEY (`Customer ID`));

CREATE TABLE `trip_planner`.`address` (
  `Address ID` INT NOT NULL AUTO_INCREMENT,
  `District` VARCHAR(45) NULL,
  `City` VARCHAR(45) NULL,
  `Pin Code` VARCHAR(45) NULL,
  `State` VARCHAR(45) NULL,
  `Country` VARCHAR(45) NULL,
  PRIMARY KEY (`Address ID`));

CREATE TABLE `trip_planner`.`hotel` (
  `Hotel ID` INT NOT NULL AUTO_INCREMENT,
  `Hotel Name` VARCHAR(45) NULL,
  `Check-in Date` DATE NULL,
  `Check-out Date` DATE NULL,
  `Room Class` VARCHAR(45) NULL,
  `Room Capacity` INT NULL,
  `Cost Per Night` INT NULL,
  `Address ID` INT NULL,
  PRIMARY KEY (`Hotel ID`),
  INDEX `FK Hotel Address_idx` (`Address ID` ASC) VISIBLE,
  CONSTRAINT `FK Hotel Address`
    FOREIGN KEY (`Address ID`)
    REFERENCES `trip_planner`.`address` (`Address ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE `trip_planner`.`transport` (
  `Transport ID` INT NOT NULL AUTO_INCREMENT,
  `Transport Type` VARCHAR(45) NULL,
  `Departure Date` DATE NULL,
  `Arrival Date` DATE NULL,
  `Start Address ID` INT NULL,
  `Destination Address ID` INT NULL,
  `Travel Time` INT NULL,
  `Price Per Seat` INT NULL,
  PRIMARY KEY (`Transport ID`),
  INDEX `FK Transport Start Address_idx` (`Start Address ID` ASC) VISIBLE,
  INDEX `FK Transport Destination Address_idx` (`Destination Address ID` ASC) VISIBLE,
  CONSTRAINT `FK Transport Start Address`
    FOREIGN KEY (`Start Address ID`)
    REFERENCES `trip_planner`.`address` (`Address ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK Transport Destination Address`
    FOREIGN KEY (`Destination Address ID`)
    REFERENCES `trip_planner`.`address` (`Address ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE `trip_planner`.`travel` (
  `Travel ID` INT NOT NULL AUTO_INCREMENT,
  `Transport ID To Destination` INT NULL,
  `Transport ID From Destination` INT NULL,
  `Number of Seats To Destination` INT NULL,
  `Number of Seats From Destination` INT NULL,
  `Total Cost` INT NULL,
  PRIMARY KEY (`Travel ID`),
  INDEX `FK Travel Transport To Destination_idx` (`Transport ID To Destination` ASC) VISIBLE,
  INDEX `FK Travel Transport From Destination_idx` (`Transport ID From Destination` ASC) VISIBLE,
  CONSTRAINT `FK Travel Transport To Destination`
    FOREIGN KEY (`Transport ID To Destination`)
    REFERENCES `trip_planner`.`transport` (`Transport ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK Travel Transport From Destination`
    FOREIGN KEY (`Transport ID From Destination`)
    REFERENCES `trip_planner`.`transport` (`Transport ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE `trip_planner`.`trip` (
  `Trip ID` INT NOT NULL AUTO_INCREMENT,
  `Customer ID` INT NULL,
  `Hotel ID` INT NULL,
  `Travel ID` INT NULL,
  `Total Cost` INT NULL,
  PRIMARY KEY (`Trip ID`),
  INDEX `FK Trip Customer_idx` (`Customer ID` ASC) VISIBLE,
  INDEX `FK Trip Hotel_idx` (`Hotel ID` ASC) VISIBLE,
  INDEX `FK Trip Travel_idx` (`Travel ID` ASC) VISIBLE,
  CONSTRAINT `FK Trip Customer`
    FOREIGN KEY (`Customer ID`)
    REFERENCES `trip_planner`.`customer` (`Customer ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK Trip Hotel`
    FOREIGN KEY (`Hotel ID`)
    REFERENCES `trip_planner`.`hotel` (`Hotel ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK Trip Travel`
    FOREIGN KEY (`Travel ID`)
    REFERENCES `trip_planner`.`travel` (`Travel ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

use trip_planner;

DELIMITER //
CREATE TRIGGER calculate_trip_cost
BEFORE INSERT ON trip_planner.trip
FOR EACH ROW
BEGIN
    DECLARE travel_cost INT;
    DECLARE hotel_cost INT;

    SELECT `Total Cost` INTO travel_cost
    FROM trip_planner.travel
    WHERE `Travel ID` = NEW.`Travel ID`;

    SELECT DATEDIFF(`Check-out Date`, `Check-in Date`) * `Cost Per Night` INTO hotel_cost
    FROM trip_planner.hotel
    WHERE `Hotel ID` = NEW.`Hotel ID`;

    SET NEW.`Total Cost` = travel_cost + hotel_cost;
END;
//
DELIMITER ;
