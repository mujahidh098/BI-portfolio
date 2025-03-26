CREATE TABLE UnitTypes (
  id int NOT NULL AUTO_INCREMENT,
  name varchar(255) NOT NULL,
  shorthand varchar(255) NOT NULL,
  isBaseUnitOfMeasure tinyint(1) NOT NULL DEFAULT '0',
  baseUnitTypeId int DEFAULT NULL,
  createdAt datetime NOT NULL,
  updatedAt datetime NOT NULL,
  deletedAt datetime DEFAULT NULL,
  createdBy int DEFAULT NULL,
  synced tinyint(1) DEFAULT '0',
  PRIMARY KEY (id),
  KEY createdBy (createdBy),
  CONSTRAINT UnitTypes_ibfk_1 FOREIGN KEY (createdBy) REFERENCES Users (id) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=latin1;


INSERT INTO UnitTypes (id, name, shorthand, createdAt, updatedAt) VALUES
(1, 'Pieces', 'pcs', NOW(), NOW()),
(2, 'Grams', 'g', NOW(), NOW()),
(3, 'Slices', 'slices', NOW(), NOW()),
(4, 'Milliliters', 'ml', NOW(), NOW()),
(5, 'Liters', 'L', NOW(), NOW());