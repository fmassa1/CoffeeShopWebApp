-- Truncate all tables and reset identity
TRUNCATE TABLE 
    Order_Items,
    Orders,
    Accounting,
    Ingredients,
    Preperation_Step,
    Recipe,
    Menu,
    Inventory,
    Work_Schedule,
    Barista,
    Manager,
    Employees
RESTART IDENTITY CASCADE;

INSERT INTO Accounting (timestamp, balance) VALUES
('2025-04-01 04:05:06', 100.00, "initial balance");

-- First, insert into Menu table (Menu should exist before Recipe)
INSERT INTO Menu (name, size, temperature, price, type) VALUES
('Latte', 'Large', 'Cold', '5.00', 'Coffee'),
('Cappucino', 'Large', 'Hot', '4.00', 'Coffee'),
('Green Tea', 'Medium', 'Hot', '3.00', 'Tea'),
('Thai Tea', 'Medium', 'Cold', '4.00', 'Tea');

-- Insert into Recipe table (Recipe should reference Menu)
INSERT INTO Recipe (name) VALUES
('Latte'),
('Cappucino'),
('Green Tea'),
('Thai Tea');

-- Insert into Inventory table
INSERT INTO Inventory (name, stock_quantity, unit, price_per_unit) VALUES
('Ice Cubes', 1000, 'oz', 0.01),
('Water', 10000, 'fl.oz', 0.01),
('Milk', 1000, 'fl.oz.', 0.50),
('Sugar', 1000, 'oz', 0.10),
('Cream', 1000, 'fl.oz', 0.75),
('Espresso Beans', 100, 'lb', 5.00),
('Green Tea Leaves', 100, 'packet', 1.00),
('Lemon Juice', 100, 'fl.oz', 0.50),
('Thai Tea Mix', 100, 'packet', 0.75),
('Half and Half', 1000, 'fl.oz', 0.75);

-- Insert into Ingredients table (now that Menu and Recipe exist)
INSERT INTO Ingredients (recipe, name, quantity) VALUES
('Latte', 'Espresso Beans', 0.05),
('Latte', 'Milk', 8),
('Latte', 'Sugar', 0.15),
('Latte', 'Cream', 0.15),
('Latte', 'Ice Cubes', 8),
('Cappucino', 'Espresso Beans', 0.05),
('Cappucino', 'Milk', 4),
('Cappucino', 'Cream', 4),
('Cappucino', 'Sugar', 0.15), 
('Green Tea', 'Water', 16),
('Green Tea', 'Green Tea Leaves', 1),
('Green Tea', 'Lemon Juice', 0.15),
('Thai Tea', 'Water', 16),
('Thai Tea', 'Thai Tea Mix', 1),
('Thai Tea', 'Milk', 1),
('Thai Tea', 'Half and Half', 1),
('Thai Tea', 'Sugar', 0.5),
('Thai Tea', 'Ice Cubes', 8);
