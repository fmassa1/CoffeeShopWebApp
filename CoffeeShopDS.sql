DROP TABLE IF EXISTS Accounts, Employees, Orders, Order_Items, Manager, Barista, Work_Schedule, Inventory, Menu, Recipe, Accounting, Ingredients, Preperation_Step;

-- Employees Table
CREATE TABLE Employees (
    name TEXT NOT NULL,
    ssn NUMERIC(9,0) NOT NULL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    salary FLOAT
);

-- Manager Table
CREATE TABLE Manager (
    ssn NUMERIC(9,0) PRIMARY KEY,
    ownership_percentage DECIMAL(5, 2),
    FOREIGN KEY (ssn) REFERENCES Employees(ssn)
);

-- Barista Table
CREATE TABLE Barista (
    ssn NUMERIC(9,0) PRIMARY KEY,
    FOREIGN KEY (ssn) REFERENCES Employees(ssn)
);

-- Work_Schedule Table
CREATE TABLE Work_Schedule (
    schedule_id SERIAL PRIMARY KEY,
    ssn NUMERIC(9,0),
    start_time TIME,
    end_time TIME,
    day_of_week VARCHAR(10),
    FOREIGN KEY (ssn) REFERENCES Barista(ssn)
);

-- Inventory Table
CREATE TABLE Inventory (
    name TEXT NOT NULL PRIMARY KEY,
    stock_quantity NUMERIC(10,2),
    unit TEXT NOT NULL,
    price_per_unit NUMERIC(10,2)
    -- CHECK (unit IN ('ounce', 'lb'))
);

-- Menu Table
CREATE TABLE Menu (
    name TEXT NOT NULL PRIMARY KEY,
    size TEXT,
    temperature TEXT,
    price TEXT,
    type TEXT,
    CHECK (temperature IN ('Cold', 'Hot')),
    CHECK (type IN ('Tea', 'Coffee', 'Soft Drink'))
);

-- Recipe Table
CREATE TABLE Recipe (
    name TEXT NOT NULL PRIMARY KEY,
    FOREIGN KEY (name) REFERENCES Menu(name)
);

-- Preperation_Step Table
CREATE TABLE Preperation_Step (
    recipe TEXT NOT NULL,
    position NUMERIC(9,0) NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (recipe) REFERENCES Recipe(name),
    PRIMARY KEY(recipe, position)
);

-- Ingredients Table
CREATE TABLE Ingredients(
    recipe TEXT NOT NULL,
    name TEXT NOT NULL,
    quantity NUMERIC(10,2),
    FOREIGN KEY (recipe) REFERENCES Recipe(name),
    FOREIGN KEY (name) REFERENCES Inventory(name),
    PRIMARY KEY(recipe, name)
);

-- Accounting Table
CREATE TABLE Accounting(
    timestamp TIMESTAMP NOT NULL PRIMARY KEY,
    balance NUMERIC(10,2) NOT NULL,
    transaction_type TEXT NOT NULL
);

-- Order_Items Table
CREATE TABLE Order_Items (
    timestamp TIMESTAMP NOT NULL,
    item TEXT NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY (timestamp, item),
    -- FOREIGN KEY (timestamp) REFERENCES Accounting(timestamp),
    FOREIGN KEY (item) REFERENCES Menu(name)
);

-- Orders Table
CREATE TABLE Orders (
    timestamp TIMESTAMP NOT NULL PRIMARY KEY,
    payment_method TEXT NOT NULL,
    -- FOREIGN KEY (timestamp) REFERENCES Accounting(timestamp),
    -- FOREIGN KEY (timestamp) REFERENCES Order_Items(timestamp),
    CHECK (payment_method IN ('cash', 'credit card', 'app'))
);

-- Accounts Table
CREATE TABLE Accounts (
    ssn NUMERIC(9,0) PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    FOREIGN KEY (ssn) REFERENCES Employees(ssn),
    FOREIGN KEY (email) REFERENCES Employees(email) ON UPDATE CASCADE
);
