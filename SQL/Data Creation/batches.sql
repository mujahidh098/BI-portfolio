CREATE TABLE Batches (
  id int unsigned NOT NULL AUTO_INCREMENT,
  sourceId int NOT NULL,
  stockItemStockCode varchar(255) NOT NULL,
  quantityOnHand decimal(12,3) DEFAULT NULL,
  originalQuantity decimal(12,3) DEFAULT NULL,
  originalQuantityLessWaste decimal(12,3) DEFAULT NULL,
  wastePercentage decimal(4,2) NOT NULL DEFAULT '0.00',
  batchPrice decimal(11,2) NOT NULL,
  unitCost decimal(11,6) NOT NULL,
  createdAt datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updatedAt datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  unitTypeId int NOT NULL,
  createdBy int NOT NULL,
  batchStatus enum('WAITING','ACTIVE','DEPLETED','LOCKED') DEFAULT 'WAITING',
  sourceType enum('DELIVERY_INCREASE','PRODUCTION_INCREASE','PRODUCTION_DECREASE','TRANSFER_DECREASE','WASTE','ORDER','STOCKTAKE_DECREASE','STOCKTAKE_INCREASE','STORE_SETUP_STOCKTAKE_INCREASE','VOID_ORDER','TRANSFER_INCREASE','DELIVERY_DECREASE','STOCK_RETURN','CREDIT_NOTE_DECREASE','CREDIT_NOTE_INCREASE','REVERSE_TRANSFER_INCREASE','REVERSE_TRANSFER_DECREASE','REVERSE_WASTE') DEFAULT NULL,
  isHoldingBatch tinyint NOT NULL DEFAULT '0',
  stockItemId int unsigned DEFAULT NULL,
  PRIMARY KEY (id),
  KEY unitTypeId (unitTypeId),
  KEY createdBy (createdBy),
  KEY idx_stockItemId (stockItemId),
  CONSTRAINT Batches_ibfk_4 FOREIGN KEY (createdBy) REFERENCES Users (id) ON UPDATE CASCADE,
  CONSTRAINT fk_stockItemId_batch FOREIGN KEY (stockItemId) REFERENCES StockItems (id)
) ENGINE=InnoDB AUTO_INCREMENT=2450 DEFAULT CHARSET=latin1;


INSERT INTO Batches (
    id, sourceId, stockItemStockCode, quantityOnHand, originalQuantity, originalQuantityLessWaste, wastePercentage, batchPrice, unitCost, createdAt, updatedAt, unitTypeId, createdBy, batchStatus, sourceType, isHoldingBatch, stockItemId) VALUES
(2200, 9710, 'BUN001', 250.500, 300.000, 285.000, 5.00, 350.00, 25.500000, '2025-02-15 12:30:00', NULL, 15, 10, 'ACTIVE', 'DELIVERY_INCREASE', 0, 150),
(2201, 9710, 'BEEF001', 180.200, 200.000, 190.000, 2.00, 400.00, 30.250000, '2025-02-20 18:45:00', NULL, 20, 10, 'WAITING', 'PRODUCTION_INCREASE', 1, 200),
(2202, 9710, 'LETT001', 400.750, 450.000, 427.500, 5.00, 200.00, 15.750000, '2025-02-05 09:15:00', NULL, 30, 10, 'DEPLETED', 'PRODUCTION_DECREASE', 0, 250),
(2203, 9710, 'TOMA001', 320.100, 350.000, 332.500, 5.00, 280.00, 20.000000, '2025-02-25 15:00:00', NULL, 5, 10, 'LOCKED', 'TRANSFER_DECREASE', 1, 300),
(2204, 9710, 'CHEESE001', 120.900, 150.000, 142.500, 5.00, 180.00, 12.500000, '2025-02-10 11:00:00', NULL, 10, 10, 'ACTIVE', 'WASTE', 0, 100),
(2205, 9710, 'SAUCE001', 450.300, 500.000, 475.000, 5.00, 220.00, 18.000000, '2025-02-18 14:30:00', NULL, 25, 10, 'WAITING', 'ORDER', 1, 125),
(2206, 9710, 'COLA001', 280.600, 320.000, 304.000, 5.00, 300.00, 22.000000, '2025-02-08 10:45:00', NULL, 35, 10, 'DEPLETED', 'STOCKTAKE_DECREASE', 0, 175),
(2207, 9710, 'FRIES001', 150.400, 180.000, 171.000, 5.00, 250.00, 19.500000, '2025-02-22 16:15:00', NULL, 1, 10, 'LOCKED', 'STOCKTAKE_INCREASE', 1, 225),
(2208, 9710, 'WRAP001', 380.800, 420.000, 399.000, 5.00, 210.00, 16.500000, '2025-02-12 13:00:00', NULL, 18, 10, 'ACTIVE', 'STORE_SETUP_STOCKTAKE_INCREASE', 0, 275),
(2209, 9710, 'ONION001', 200.700, 220.000, 209.000, 5.00, 230.00, 18.500000, '2025-02-28 17:30:00', NULL, 8, 10, 'WAITING', 'VOID_ORDER', 1, 325);
