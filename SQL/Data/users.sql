CREATE TABLE Users (
  id int NOT NULL AUTO_INCREMENT,
  createdAt datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updatedAt datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deletedAt datetime DEFAULT NULL,
  uuid char(36) CHARACTER SET latin1 COLLATE latin1_bin NOT NULL,
  email varchar(255) NOT NULL,
  password varchar(255) NOT NULL,
  code varchar(255) DEFAULT NULL,
  cellphone varchar(255) NOT NULL,
  firstName varchar(255) NOT NULL,
  lastName varchar(255) NOT NULL,
  dateOfBirth date DEFAULT NULL,
  isDeleted tinyint(1) NOT NULL DEFAULT '0',
  isAdmin tinyint(1) NOT NULL DEFAULT '0',
  groupId int DEFAULT NULL,
  synced tinyint(1) NOT NULL DEFAULT '0',
  rate decimal(12,2) DEFAULT NULL,
  overtimeRate decimal(12,2) DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uuid (uuid),
  KEY groupId (groupId),
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;


INSERT INTO Users (id, email, password, cellphone, firstName, lastName, uuid) VALUES
(1, 'user1@example.com', 'password1', '123-456-7890', 'John', 'Doe', UUID()),
(2, 'user2@example.com', 'password2', '987-654-3210', 'Jane', 'Smith', UUID()),
(10, 'user3@example.com', 'password3', '555-123-4567', 'Alice', 'Johnson', UUID());