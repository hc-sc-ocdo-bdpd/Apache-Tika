-- =====================================================
-- Sample SQL Database
-- =====================================================

-- Drop tables if they already exist (order matters due to FK constraints)
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

-- =====================================================
-- Customers Table
-- =====================================================
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name  VARCHAR(50) NOT NULL,
    last_name   VARCHAR(50) NOT NULL,
    email       VARCHAR(100) UNIQUE,
    created_at  DATE
);

-- =====================================================
-- Products Table
-- =====================================================
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category     VARCHAR(50),
    price        DECIMAL(10, 2) NOT NULL,
    in_stock     INTEGER
);

-- =====================================================
-- Orders Table
-- =====================================================
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id  INTEGER NOT NULL,
    order_date  DATE,
    quantity    INTEGER,
    total_price DECIMAL(10, 2),

    -- Foreign key constraints
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id)  REFERENCES products(product_id)
);

-- =====================================================
-- Insert Sample Customers
-- =====================================================
INSERT INTO customers (customer_id, first_name, last_name, email, created_at) VALUES
(1, 'Alice', 'Nguyen', 'alice.nguyen@example.com', '2024-01-15'),
(2, 'Bob', 'Smith', 'bob.smith@example.com', '2024-02-03'),
(3, 'Carol', 'Martinez', 'carol.martinez@example.com', '2024-02-20');

-- =====================================================
-- Insert Sample Products
-- =====================================================
INSERT INTO products (product_id, product_name, category, price, in_stock) VALUES
(101, 'Wireless Mouse', 'Electronics', 29.99, 120),
(102, 'Mechanical Keyboard', 'Electronics', 89.99, 75),
(103, 'Water Bottle', 'Accessories', 14.50, 200);

-- =====================================================
-- Insert Sample Orders
-- =====================================================
INSERT INTO orders (order_id, customer_id, product_id, order_date, quantity, total_price) VALUES
(1001, 1, 101, '2024-03-01', 2, 59.98),
(1002, 2, 102, '2024-03-05', 1, 89.99),
(1003, 1, 103, '2024-03-10', 3, 43.50),
(1004, 3, 101, '2024-03-12', 1, 29.99);

-- =====================================================
-- Example Queries (optional)
-- =====================================================

-- View all customers
-- SELECT * FROM customers;

-- View all orders with customer names
-- SELECT
--     o.order_id,
--     c.first_name || ' ' || c.last_name AS customer_name,
--     p.product_name,
--     o.quantity,
--     o.total_price
-- FROM orders o
-- JOIN customers c ON o.customer_id = c.customer_id
-- JOIN products p ON o.product_id = p.product_id;
