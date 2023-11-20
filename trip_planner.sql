CREATE SCHEMA `trip_planner` ;

CREATE TABLE `trip_planner`.`customer` (
  `customer_id` INT NOT NULL,
  `customer_name` VARCHAR(45) NULL,
  `password` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  PRIMARY KEY (`customer_id`));

CREATE TABLE `trip_planner`.`cust_phone` (
  `phno` VARCHAR(10) NOT NULL,
  `customer_id` INT NULL,
  PRIMARY KEY (`phno`),
  INDEX `fk_customer_phone_idx` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `fk_customer_phone`
    FOREIGN KEY (`customer_id`)
    REFERENCES `trip_planner`.`customer` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE `trip_planner`.`Travel` (
  `travel_id` INT NOT NULL,
  `vehicle_id_to` INT NULL,
  `vehicle_id_from` INT NULL,
  `vehicle_quantity_from` INT NULL,
  `vehicle_quantity_to` INT NULL,
  `Total_cost` INT NULL,
  PRIMARY KEY (`travel_id`));


CREATE TABLE `trip_planner`.`Address` (
  `Address_id` INT NOT NULL,
  `location_name` VARCHAR(45) NULL,
  `pincode` VARCHAR(45) NULL,
  `country` VARCHAR(45) NULL,
  `house_no` VARCHAR(45) NULL,
  `street_no` VARCHAR(45) NULL,
  `locality` VARCHAR(45) NULL,
  `landmark` VARCHAR(45) NULL,
  PRIMARY KEY (`Address_id`));

CREATE TABLE `trip_planner`.`vehicle` (
  `vehicle_id` INT NOT NULL,
  `arriving_date` DATE NULL,
  `vehicle_type` VARCHAR(45) NULL,
  `leaving_date` DATE NULL,
  `start_address_id` INT NULL,
  `dest_address_id` INT NULL,
  `Address_id` INT NULL,
  PRIMARY KEY (`vehicle_id`),
  INDEX `fk_vehicle_1_idx` (`Address_id` ASC) VISIBLE,
  CONSTRAINT `fk_vehicle_1`
    FOREIGN KEY (`Address_id`)
    REFERENCES `trip_planner`.`Address` (`Address_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE `trip_planner`.`flights` (
  `flight_number` INT NOT NULL,
  `price_per_seat` FLOAT NULL,
  `number_seats` INT NULL,
  `airline` VARCHAR(45) NULL,
  `description` VARCHAR(45) NULL,
  `seat_class` VARCHAR(45) NULL,
  `duration_mins` INT NULL,
  `vehicle_id` INT NULL,
  PRIMARY KEY (`flight_number`),
  INDEX `fk_flights_1_idx` (`vehicle_id` ASC) VISIBLE,
  CONSTRAINT `fk_flights_1`
    FOREIGN KEY (`vehicle_id`)
    REFERENCES `trip_planner`.`vehicle` (`vehicle_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


CREATE TABLE `trip_planner`.`buses` (
  `vehicle_number` INT NOT NULL,
  `description` VARCHAR(45) NULL,
  `duration_mins` INT NULL,
  `seat_class` VARCHAR(45) NULL,
  `travel_agency` VARCHAR(45) NULL,
  `number_seats` INT NULL,
  `price_per_seat` FLOAT NULL,
  `vehicle_id` INT NULL,
  PRIMARY KEY (`vehicle_number`),
  INDEX `fk_buses_1_idx` (`vehicle_id` ASC) VISIBLE,
  CONSTRAINT `fk_buses_1`
    FOREIGN KEY (`vehicle_id`)
    REFERENCES `trip_planner`.`vehicle` (`vehicle_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);




CREATE TABLE `trip_planner`.`Hotels` (
  `Hotel_id` INT NOT NULL,
  `room_id` VARCHAR(45) NULL,
  `hotel_name` VARCHAR(45) NULL,
  `check_in_date` DATE NULL,
  `check_out_date` DATE NULL,
  `room_capacity` INT NULL,
  `room_class` VARCHAR(45) NULL,
  `cost_per_night` FLOAT NULL,
  `Address_id` INT NULL,
  PRIMARY KEY (`Hotel_id`),
  INDEX `fk_Hotels_1_idx` (`Address_id` ASC) VISIBLE,
  CONSTRAINT `fk_Hotels_1`
    FOREIGN KEY (`Address_id`)
    REFERENCES `trip_planner`.`Address` (`Address_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
    
    
    
CREATE TABLE `trip_planner`.`booking` (
  `No_of_rooms` INT NOT NULL,
  `Total_cost` FLOAT NULL,
  `Hotel_Id` INT NULL,
  `customer_id` INT NULL,
  `travel_id` INT NULL,
  PRIMARY KEY (`No_of_rooms`),
  INDEX `fk_booking_1_idx` (`Hotel_Id` ASC) VISIBLE,
  INDEX `fk_booking_2_idx` (`customer_id` ASC) VISIBLE,
  INDEX `fk_booking_3_idx` (`travel_id` ASC) VISIBLE,
  CONSTRAINT `fk_booking_1`
    FOREIGN KEY (`Hotel_Id`)
    REFERENCES `trip_planner`.`Hotels` (`Hotel_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_booking_2`
    FOREIGN KEY (`customer_id`)
    REFERENCES `trip_planner`.`customer` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_booking_3`
    FOREIGN KEY (`travel_id`)
    REFERENCES `trip_planner`.`Travel` (`travel_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


