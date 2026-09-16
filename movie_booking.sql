-- ============================================================
-- Movie Ticket Booking & Management System
-- DBMS Project SQL Database Script for MySQL
-- Database: movie_booking_db
-- ============================================================

-- Step 1: Create Database
CREATE DATABASE IF NOT EXISTS movie_booking_db;
USE movie_booking_db;

-- Step 2: Drop existing tables if re-importing (Child table first, then Parent tables)
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS movies;

-- Step 3: Create 'movies' Table
CREATE TABLE movies (
    movie_id INT PRIMARY KEY AUTO_INCREMENT,
    movie_name VARCHAR(100) NOT NULL,
    genre VARCHAR(50) NOT NULL,
    language VARCHAR(50) NOT NULL,
    duration VARCHAR(50) NOT NULL,
    rating DECIMAL(3, 1) NOT NULL
);

-- Step 4: Create 'customers' Table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL
);

-- Step 5: Create 'bookings' Table (With Foreign Keys)
CREATE TABLE bookings (
    booking_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    movie_id INT NOT NULL,
    booking_date DATE NOT NULL,
    show_time VARCHAR(20) NOT NULL,
    tickets INT NOT NULL,
    seat_type VARCHAR(20) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'Confirmed',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE
);

-- Step 6: Insert Sample Movies (6 Movies required)
INSERT INTO movies (movie_name, genre, language, duration, rating) VALUES
('Avengers: Endgame', 'Action / Sci-Fi', 'English', '181 min', 8.4),
('Interstellar', 'Sci-Fi / Drama', 'English', '169 min', 8.7),
('3 Idiots', 'Comedy / Drama', 'Hindi', '170 min', 8.4),
('Dangal', 'Biography / Drama', 'Hindi', '161 min', 8.3),
('Inception', 'Sci-Fi / Action', 'English', '148 min', 8.8),
('Spider-Man: No Way Home', 'Action / Sci-Fi', 'English', '148 min', 8.2);

-- Step 7: Insert Sample Customers (For initial demonstration)
INSERT INTO customers (customer_name, email, phone) VALUES
('Rahul Sharma', 'rahul@gmail.com', '9876543210'),
('Priya Patel', 'priya@gmail.com', '9812345678');

-- Step 8: Insert Sample Bookings (For initial demonstration)
INSERT INTO bookings (customer_id, movie_id, booking_date, show_time, tickets, seat_type, total_amount, status) VALUES
(1, 1, CURDATE(), '4:00 PM', 2, 'Premium', 500.00, 'Confirmed'),
(2, 3, CURDATE(), '7:00 PM', 3, 'Regular', 450.00, 'Confirmed');

-- Verification Query
SELECT 'Movies Inserted:' AS Message, COUNT(*) AS Total FROM movies;
SELECT 'Customers Inserted:' AS Message, COUNT(*) AS Total FROM customers;
SELECT 'Bookings Inserted:' AS Message, COUNT(*) AS Total FROM bookings;
