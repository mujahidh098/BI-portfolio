CREATE TABLE StockCategories (
  id int unsigned NOT NULL AUTO_INCREMENT,
  externalID bigint unsigned DEFAULT NULL,
  name varchar(255) NOT NULL,
  createdAt datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updatedAt datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  createdBy int DEFAULT NULL,
  synced tinyint(1) DEFAULT '0',
  PRIMARY KEY (id),
  UNIQUE KEY externalID (externalID),
  KEY createdBy (createdBy),
  CONSTRAINT StockCategories_ibfk_1 FOREIGN KEY (createdBy) REFERENCES Users (id) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=282 DEFAULT CHARSET=latin1;


INSERT INTO StockCategories (externalID, name, createdAt, updatedAt, createdBy, synced) VALUES
(1001, 'Buns', NOW(), NULL, 1, 0),
(1002, 'Meats', NOW(), NULL, 2, 0),
(1003, 'Vegetables', NOW(), NULL, 3, 0),
(1004, 'Sauces', NOW(), NULL, 1, 0),
(1005, 'Drinks', NOW(), NULL, 2, 0),
(1006, 'Sides', NOW(), NULL, 3, 0),
(1007, 'Packaging', NOW(), NULL, 1, 0),
(1008, 'Dairy', NOW(), NULL, 2, 0);