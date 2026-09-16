# 🎬 Movie Ticket Booking & Management System

<p align="center">

### A modern and simple movie ticket booking platform

**Built with Python Flask · MySQL · MongoDB · HTML · CSS · JavaScript**

</p>

---

## 🌟 Overview

The application combines a structured **MySQL database** for movies, customers, and bookings with **MongoDB** for flexible movie review data.

The result is a lightweight, responsive, and database-driven movie booking experience.

---

## ✨ Features

### 🎬 Movie Discovery

* Browse available movies
* View movie information
* Genre and language details
* Movie duration
* Ratings
* Quick booking access

### 🎟️ Ticket Booking

Users can:

* Select a movie
* Choose a date
* Select a show time
* Choose seat type
* Select ticket quantity
* View automatically calculated total amount
* Confirm a booking

### 👤 Customer Management

* Store customer information
* Manage customer booking records
* Connect customers with their reservations

### 📋 Booking Management

* View all bookings
* Search bookings
* View booking details
* Track booking status
* Cancel bookings

### ⭐ Reviews & Ratings

Users can:

* Select a movie
* Give a 1–5 star rating
* Write a review
* Submit feedback
* View previously submitted reviews

Reviews are stored as flexible documents in MongoDB.

---

# 🛠️ Technology Stack

| Layer               | Technology              |
| ------------------- | ----------------------- |
| Frontend            | HTML5, CSS3, JavaScript |
| Backend             | Python Flask            |
| Relational Database | MySQL                   |
| NoSQL Database      | MongoDB                 |
| MySQL Driver        | mysql-connector-python  |
| MongoDB Driver      | PyMongo                 |
| Architecture        | Client–Server           |

---

# 🏗️ Architecture

```text
                         👤 USER
                           │
                           ▼
                ┌────────────────────┐
                │   WEB INTERFACE    │
                │ HTML · CSS · JS    │
                └──────────┬─────────┘
                           │
                           ▼
                ┌────────────────────┐
                │    FLASK SERVER    │
                │   PYTHON BACKEND   │
                └──────────┬─────────┘
                           │
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
        ┌────────────────┐   ┌────────────────┐
        │     MySQL      │   │    MongoDB     │
        │   Relational   │   │     NoSQL      │
        └───────┬────────┘   └───────┬────────┘
                │                    │
                ▼                    ▼
        Movies · Customers       Movie Reviews
             · Bookings
```

---

# 🗃️ Data Management

## MySQL

MySQL manages structured application data.

### Database

```text
movie_booking_db
```

### Tables

```text
movie_booking_db
│
├── movies
├── customers
└── bookings
```

### Movies

| Field        | Description             |
| ------------ | ----------------------- |
| `movie_id`   | Unique movie identifier |
| `movie_name` | Movie title             |
| `genre`      | Movie category          |
| `language`   | Movie language          |
| `duration`   | Movie duration          |
| `rating`     | Movie rating            |

### Customers

| Field           | Description                |
| --------------- | -------------------------- |
| `customer_id`   | Unique customer identifier |
| `customer_name` | Customer name              |
| `email`         | Email address              |
| `phone`         | Contact number             |

### Bookings

| Field          | Description               |
| -------------- | ------------------------- |
| `booking_id`   | Unique booking identifier |
| `customer_id`  | Customer reference        |
| `movie_id`     | Movie reference           |
| `booking_date` | Date of booking           |
| `show_time`    | Selected show             |
| `tickets`      | Number of tickets         |
| `seat_type`    | Regular / Premium         |
| `total_amount` | Booking amount            |
| `status`       | Confirmed / Cancelled     |

---

# 🍃 MongoDB

MongoDB is used for flexible movie review and feedback data.

### Database

```text
movie_booking_nosql
```

### Collection

```text
reviews
```

Example document:

```json
{
  "customer_name": "Samar",
  "movie_name": "Inception",
  "rating": 5,
  "comment": "Amazing background score and plot!",
  "created_at": "2026-09-16 18:20"
}
```

---

# 🔗 Data Relationships

The booking system maintains relationships between customers, movies, and bookings.

```text
       CUSTOMERS
           │
           │ customer_id
           ▼
       BOOKINGS
           ▲
           │ movie_id
           │
         MOVIES
```

### Relationships

```text
customers.customer_id
          ↓
bookings.customer_id

movies.movie_id
          ↓
bookings.movie_id
```

This structure keeps customer, movie, and booking information organized and reduces unnecessary duplication.

---

# 📁 Project Structure

```text
movie-booking/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── index.html
│   ├── movies.html
│   ├── book.html
│   ├── bookings.html
│   └── reviews.html
│
├── static/
│   ├── style.css
│   └── script.js
│
└── database/
    └── movie_booking.sql
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate to the project:

```bash
cd movie-booking
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:

```text
Flask
mysql-connector-python
pymongo
```

---

## 3. Configure MySQL

Create the database:

```sql
CREATE DATABASE movie_booking_db;
```

Import the SQL file:

```text
database/movie_booking.sql
```

Verify the database:

```sql
USE movie_booking_db;

SELECT * FROM movies;
SELECT * FROM customers;
SELECT * FROM bookings;
```

---

## 4. Configure MongoDB

Start your local MongoDB server.

Connection:

```text
mongodb://localhost:27017/
```

Create:

```text
Database:
movie_booking_nosql

Collection:
reviews
```

---

## 5. Configure Application

Update your database credentials in the configuration file:

```python
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "YOUR_MYSQL_PASSWORD"
MYSQL_DATABASE = "movie_booking_db"

MONGO_URI = "mongodb://localhost:27017/"
```

Replace `YOUR_MYSQL_PASSWORD` with your MySQL password.

---

# ▶️ Running 

Start the Flask application:

```bash
python app.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

Open the address in your browser.

---

# 🎥 Application Workflow

### 01 — Discover

Browse available movies and explore their details.

↓

### 02 — Select

Choose a movie, date, show time, and seat type.

↓

### 03 — Book

Enter customer details and confirm the ticket booking.

↓

### 04 — Manage

View existing bookings and cancel reservations when required.

↓

### 05 — Review

Rate movies and share feedback.

↓

### 06 — Store

Booking information is stored in MySQL while reviews are stored in MongoDB.

---

# 🔄 Data Flow

## 🎟️ Booking

```text
Customer
   ↓
Booking Form
   ↓
Flask Backend
   ↓
MySQL
   ↓
Booking Record
```

## ⭐ Review

```text
Customer
   ↓
Review Form
   ↓
Flask Backend
   ↓
MongoDB
   ↓
Review Document
```

---

# 🧠 Database Strategy

### MySQL

Used for structured and relational information:

* 🎬 Movies
* 👤 Customers
* 🎟️ Bookings

### MongoDB

Used for flexible information:

* ⭐ Reviews
* 💬 Comments
* 📊 Ratings
* 🕒 Review timestamps

Using the two databases allows each type of information to be managed according to its structure and requirements.

---

# 📊 CRUD Operations

The application supports standard data operations.

### Create

* Add movie
* Add customer
* Create booking
* Submit review

### Read

* View movies
* View bookings
* View reviews

### Update

* Update booking status
* Cancel booking

### Delete

* Remove records where required

---

# 🧪 Example Booking

```text
Customer:
Samar

Movie:
Inception

Tickets:
2

Seat Type:
Regular

Total:
₹300

Status:
Confirmed
```

---

# ⭐ Example Review

```text
Customer:
Samar

Movie:
Inception

Rating:
★★★★★

Comment:
Amazing background score and plot!
```

MongoDB document:

```json
{
  "customer_name": "Samar",
  "movie_name": "Inception",
  "rating": 5,
  "comment": "Amazing background score and plot!"
}
```

---

# 🔐 Data Integrity

The relational database maintains consistency using:

* Primary Keys
* Foreign Keys
* Data Types
* Constraints
* Relational structure
* Transactions

MongoDB provides flexible document storage for reviews and feedback.

---

# 🎯 Key Highlights

```text
✓ Clean Web Interface
✓ Movie Management
✓ Customer Management
✓ Ticket Booking
✓ Booking Cancellation
✓ Automatic Price Calculation
✓ Movie Reviews
✓ MySQL Integration
✓ MongoDB Integration
✓ CRUD Operations
✓ Responsive Design
```

---

# 📚 What This Project Demonstrates

* Full-stack web application development
* Python backend development
* Flask routing
* MySQL database integration
* MongoDB integration
* Relational database design
* NoSQL document storage
* CRUD operations
* Frontend–backend communication
* Database-driven application development

---

# 📜 License

This project is provided for educational and personal development purposes.

---

<p align="center">
