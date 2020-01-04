DROP TABLE IF EXISTS `flags`;
DROP TABLE IF EXISTS `nutrition`;
DROP TABLE IF EXISTS `foods`;
CREATE TABLE `foods` (
	`id` INT NOT NULL,
	`name` varchar(55) NOT NULL,
	`date` DATE NOT NULL,
	`category` varchar(55),
	`meal` varchar(10) NOT NULL,
	`location` varchar(10) NOT NULL,
	PRIMARY KEY (`id`)
);


CREATE TABLE `nutrition` (
	`id` INT NOT NULL,
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
	`id` INT NOT NULL,
	`name` varchar(20) NOT NULL,
	`type` varchar(10) NOT NULL,
	`food_id` INT NOT NULL,
	PRIMARY KEY (`id`),
    FOREIGN KEY (`food_id`)
        REFERENCES `foods` (`id`)
        ON DELETE CASCADE
);
