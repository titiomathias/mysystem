-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mysystem
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mysystem
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mysystem` DEFAULT CHARACTER SET utf8 ;
USE `mysystem` ;

-- -----------------------------------------------------
-- Table `mysystem`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mysystem`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(32) NOT NULL,
  `email` VARCHAR(128) NOT NULL,
  `password_hash` VARCHAR(64) NOT NULL,
  `level` MEDIUMINT NOT NULL DEFAULT 1,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mysystem`.`tasks`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mysystem`.`tasks` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(64) NOT NULL,
  `description` VARCHAR(512) NOT NULL,
  `category` VARCHAR(32) NOT NULL DEFAULT 'common',
  `frequency` ENUM('once', 'daily', 'weekly', 'habit') NOT NULL DEFAULT 'once',
  `base_xp` INT NOT NULL,
  `status` TINYINT NOT NULL,
  `user_id` INT NOT NULL,
  `last_completeted_at` TIMESTAMP NULL,
  `streak_count` INT NOT NULL DEFAULT 0,
  `best_streak` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  INDEX `fk_tasks_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_tasks_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `mysystem`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mysystem`.`attributes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mysystem`.`attributes` (
  `str` INT NOT NULL,
  `agi` INT NOT NULL,
  `con` INT NOT NULL,
  `wis` INT NOT NULL,
  `int` INT NOT NULL,
  `cha` INT NOT NULL,
  `user_id` INT NOT NULL,
  INDEX `fk_attributes_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_attributes_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `mysystem`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mysystem`.`task_attributes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mysystem`.`task_attributes` (
  `attribute` ENUM('cha', 'wis', 'int', 'str', 'agi', 'con') NOT NULL,
  `value` SMALLINT NOT NULL,
  `task_id` INT NOT NULL,
  INDEX `fk_task_attributes_tasks1_idx` (`task_id` ASC) VISIBLE,
  CONSTRAINT `fk_task_attributes_tasks1`
    FOREIGN KEY (`task_id`)
    REFERENCES `mysystem`.`tasks` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mysystem`.`task_logs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mysystem`.`task_logs` (
  `id` INT NOT NULL,
  `xp_earned` INT NOT NULL,
  `completed_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  `task_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `streak_at_completion` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_task_logs_tasks1_idx` (`task_id` ASC) VISIBLE,
  INDEX `fk_task_logs_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_task_logs_tasks1`
    FOREIGN KEY (`task_id`)
    REFERENCES `mysystem`.`tasks` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_task_logs_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `mysystem`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
