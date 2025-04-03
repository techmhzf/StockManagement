-- Drop existing tables if they exist
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS stocks;

-- Create Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- Create Stocks Table
CREATE TABLE stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    company TEXT NOT NULL,
    price REAL NOT NULL,
    change REAL NOT NULL
);

-- Insert Sample Users
INSERT INTO users (name, email, password) VALUES 
('John Doe', 'john@example.com', 'hashed_password1'),
('Alice Smith', 'alice@example.com', 'hashed_password2'),
('Bob Johnson', 'bob@example.com', 'hashed_password3');

-- Insert Sample Stock Data
INSERT INTO stocks (symbol, company, price, change) VALUES 
('AAPL', 'Apple Inc.', 175.6, 1.5),
('GOOGL', 'Alphabet Inc.', 2780.3, -2.3),
('TSLA', 'Tesla Inc.', 930.2, 3.2),
('MSFT', 'Microsoft Corporation', 299.8, 0.5),
('AMZN', 'Amazon.com, Inc.', 3345.0, -1.2);