-- === FOR RESETTING DATA ===
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

-- === EMPLOYEES ===
INSERT INTO Employees (name, ssn, email, salary) VALUES
('Alice Johnson', 111223333, 'alice@example.com', 52000.00),
('Bob Smith', 222334444, 'bob@example.com', 45000.00),
('Carla Diaz', 333445555, 'carla@example.com', 48000.00),
('Daniel Wu', 444556666, 'daniel@example.com', 47000.00);

-- === MANAGER ===
INSERT INTO Manager (ssn, ownership_percentage) VALUES
(111223333, 25.50),
(222334444, 10.00);

-- === BARISTA ===
INSERT INTO Barista (ssn) VALUES
(333445555),
(444556666);

-- === WORK SCHEDULE ===
INSERT INTO Work_Schedule (ssn, start_time, end_time, day_of_week) VALUES
(333445555, '08:00', '14:00', 'Monday'),
(333445555, '10:00', '16:00', 'Wednesday'),
(444556666, '12:00', '18:00', 'Tuesday'),
(444556666, '09:00', '15:00', 'Thursday');



-- === MENU ===
INSERT INTO Menu (name, size, temperature, price, type) VALUES
('Latte', 'Large', 'Cold', '5.00', 'Coffee'),
('Cappucino', 'Large', 'Hot', '4.00', 'Coffee'),
('Green Tea', 'Medium', 'Hot', '3.00', 'Tea'),
('Thai Tea', 'Medium', 'Cold', '4.00', 'Tea');

-- === RECIPE ===
INSERT INTO Recipe (name) VALUES
('Latte'),
('Cappucino'),
('Green Tea'),
('Thai Tea');

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

-- === PREPERATION STEP ===
INSERT INTO Preperation_Step (recipe, position, name) VALUES
('Latte', 1, 'Grind beans'),
('Latte', 2, 'Brew espresso'),
('Latte', 3, 'Steam milk'),
('Thai Tea', 1, 'Brew coffee'),
('Thai Tea', 2, 'Add ice'),
('Green Tea', 1, 'Boil water'),
('Green Tea', 2, 'Steep leaves');

-- === INGREDIENTS ===
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

-- === ACCOUNTING ===
INSERT INTO Accounting (timestamp, balance, transaction_type) VALUES
('2025-04-01 04:05:06', 100.00, 'initial balance');

-- === ORDERS ===
INSERT INTO Orders (timestamp, payment_method) VALUES
('2025-04-01 04:05:06', 'cash'),
('2025-04-01 04:20:06', 'credit card'),
('2025-04-01 04:25:06', 'app');

-- === ORDER ITEMS ===
INSERT INTO Order_Items (timestamp, item, quantity) VALUES
('2025-04-01 04:05:06', 'Latte', 1),
('2025-04-01 04:20:06', 'Thai Tea', 2),
('2025-04-01 04:25:06', 'Green Tea', 1);