-- ---
-- Table 'Monitors'
-- Tabela przechowująca informacje o monitorach.
-- ---

DROP TABLE IF EXISTS `Monitors`;

CREATE TABLE `Monitors` (
  `monitorID` INTEGER NOT NULL AUTO_INCREMENT,
  `address` VARCHAR(255) NOT NULL,
  `port` VARCHAR(255) NOT NULL,
  `uuid` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`monitorID`)
) COMMENT 'Tabela przechowująca informacje o monitorach.';

-- ---
-- Table 'Sensors'
-- Tabela przechowująca informacje o sensorach.
-- ---

DROP TABLE IF EXISTS `Sensors`;

CREATE TABLE `Sensors` (
  `sensorID` INTEGER NOT NULL AUTO_INCREMENT,
  `monitorUUID` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `address` VARCHAR(255) NOT NULL,
  `port` VARCHAR(255) NOT NULL,
  `cpu` BOOLEAN NOT NULL DEFAULT FALSE,
  `ram` BOOLEAN NOT NULL DEFAULT FALSE,
  `hdd` BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (`sensorID`)
) COMMENT 'Tabela przechowująca informacje o sensorach.';