-- Create Menu Categories Table
CREATE TABLE MenuCategories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    categoryName VARCHAR(255) NOT NULL
); 

-- Insert Menu Categories
INSERT INTO MenuCategories (categoryName) VALUES
('Burgers'),
('Combos');