DROP TABLE IF EXISTS `flags`;
DROP TABLE IF EXISTS `nutrition`;
DROP TABLE IF EXISTS `foods`;
CREATE TABLE `foods` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` varchar(55) NOT NULL,
	`date` DATE NOT NULL,
	`category` varchar(55),
	`meal` ENUM('breakfast','lunch','dinner','late night','grabngo') NOT NULL,
	`location` ENUM('worcester','frank','hampshire','berkshire') NOT NULL,
	PRIMARY KEY (`id`)
);


CREATE TABLE `nutrition` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`serving_size` varchar(15),
	`calories` INT,
	`calories_from_fat` INT,
	`fat` INT,
	`sat_fat` INT,
	`trans_fat` INT,
	`cholesterol` INT,
	`sodium` INT,
	`carbs` INT,
	`fiber` INT,
	`sugar` INT,
	`protein` INT,
	`ingredients` TEXT,
	`food_id` int NOT NULL,
	PRIMARY KEY (`id`),
    FOREIGN KEY (`food_id`)
        REFERENCES `foods` (`id`)
        ON DELETE CASCADE
);

CREATE TABLE `flags` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` varchar(20) NOT NULL,
	`type` ENUM('allergen', 'diet') NOT NULL,
	`food_id` INT NOT NULL,
	PRIMARY KEY (`id`),
    FOREIGN KEY (`food_id`)
        REFERENCES `foods` (`id`)
        ON DELETE CASCADE
);
