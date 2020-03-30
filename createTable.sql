CREATE TABLE `FileBlobs` (
 `path` VARCHAR(100) NOT NULL,
 `file` BLOB NOT NULL
)

CREATE TABLE `FileInfo` (
 `type` CHAR(3),
 `ownerPermission` CHAR(3),
 `groupUserPermission` CHAR(3),
 `otherUserPermission` CHAR(3),
 `numHardLinks` INT,
 `owner` VARCHAR(10),
 `group` VARCHAR(10),
 `size` INT,
 `lastModified` DATE,
 `lastModifiedTime` TIME,
 `name` VARCHAR(100) NOT NULL,
 `path` VARCHAR(100) NOT NULL
)

