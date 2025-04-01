CREATE TABLE MenuItems (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NULL,
    price DECIMAL(10,2) NOT NULL,
    categoryId INT NULL,
    FOREIGN KEY (categoryId) REFERENCES MenuCategories(id) ON DELETE SET NULL
);