-- SQL script to set up Airflow user and initialize example_db database

-- Create Airflow user
CREATE USER 'airflow'@'localhost' IDENTIFIED BY 'airflow_password';

-- Initialize example_db database
CREATE DATABASE example_db;
USE example_db;

-- Create products table
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX(name)
);

-- Insert sample data into products table
INSERT INTO products (name, price) VALUES 
('Product A', 25.50),
('Product B', 15.00),
('Product C', 10.75);

-- Create sales table
CREATE TABLE sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id),
    INDEX(sale_date)
);

-- Insert sample data into sales table
INSERT INTO sales (product_id, quantity) VALUES 
(1, 2),
(2, 1),
(3, 5);

-- Create logs table
CREATE TABLE logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    log_message TEXT NOT NULL,
    log_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX(log_date)
);

-- Insert sample log data
INSERT INTO logs (log_message) VALUES 
('Log entry 1'),
('Log entry 2'),
('Log entry 3');