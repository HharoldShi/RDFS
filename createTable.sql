CREATE DATABASE IF NOT EXISTS ece656project;
use ece656project;

drop table if exists `FileBlobs`;
CREATE TABLE `FileBlobs` (
 `parentdir` VARCHAR(256) NOT NULL,
 `name` VARCHAR(100) NOT NULL,
 `fileContent` LONGBLOB NOT NULL,
 PRIMARY KEY(`parentdir`,`name`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists `FileInfo`;
CREATE TABLE `FileInfo` (
 `parentdir` VARCHAR(256) NOT NULL,
 `name` VARCHAR(100) NOT NULL,
 `type` CHAR(1),
 `ownerPermission` CHAR(3),
 `groupUserPermission` CHAR(3),
 `otherUserPermission` CHAR(5),
 `numHardLinks` INT,
 `owner` VARCHAR(10),
 `group` VARCHAR(10),
 `size` INT,
 `lastModifiedDate` Char(8),
 `lastModifiedTime` Char(8),
 PRIMARY KEY(`parentdir`,`name`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


