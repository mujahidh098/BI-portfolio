-- Create Menu Items Table
CREATE TABLE MenuItems (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NULL,
    price DECIMAL(10,2) NOT NULL,
    categoryId INT NULL,
    FOREIGN KEY (categoryId) REFERENCES MenuCategories(id) ON DELETE SET NULL
); 


-- Insert Menu Items
INSERT INTO MenuItems (name, description, price, categoryId) VALUES
('Single Beef', 'A classic beef burger with fresh toppings.', 68.99, (SELECT id FROM MenuCategories WHERE categoryName = 'Burgers')),
('Double Beef', 'Double the beef, double the flavor.', 66.99, (SELECT id FROM MenuCategories WHERE categoryName = 'Burgers')),
('Fried Chicken', 'Crispy fried chicken burger.', 65.99, (SELECT id FROM MenuCategories WHERE categoryName = 'Burgers')),
('Combo Meal', 'Burger, fries, and a drink.', 99.99, (SELECT id FROM MenuCategories WHERE categoryName = 'Combos'));