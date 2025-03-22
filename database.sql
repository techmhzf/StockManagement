CREATE DATABASE stock_management;
USE stock_management;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE mutual_funds (
    fund_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    nav FLOAT,
    category VARCHAR(50),
    risk VARCHAR(50),
    returns FLOAT
);

CREATE TABLE user_portfolio (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    fund_id INT,
    units FLOAT,
    purchase_price FLOAT,
    purchase_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (fund_id) REFERENCES mutual_funds(fund_id)
);
