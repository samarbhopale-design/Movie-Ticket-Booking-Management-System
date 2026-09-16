# 🎬 Movie Ticket Booking & Management System
> **A Hybrid SQL + NoSQL**

---

## 📌 Project Overview
**Movie Ticket Booking & Management System** is a clean, simple, and modern to demonstrate dual-database integration in a web application:
- **Relational SQL Database (MySQL)** is used for structured, transactional data (**Movies**, **Customers**, and **Bookings**).
- **Document NoSQL Database (MongoDB)** is used for unstructured, high-frequency user feedback (**Movie Reviews**).

The application is built using standard Python **Flask**, plain **HTML5/CSS3/JavaScript**, **`mysql-connector-python`**, and **`pymongo`**.

---

## 🛠️ Technology Requirements

- **Frontend:** HTML5, CSS3 (Modern Cinema Dark Theme), Simple Vanilla JavaScript
- **Backend:** Python 3, Flask Framework
- **SQL Database:** MySQL Server (`movie_booking_db`)
- **NoSQL Database:** MongoDB Server (`movie_booking_nosql`)
- **Python Libraries:** `Flask`, `mysql-connector-python`, `pymongo`

---

## 📂 Project Structure

```text
samar dbms/
├── app.py                  # Flask backend & application routes
├── config.py               # Database connection configurations
├── requirements.txt        # Python package dependencies
├── README.md               # Project documentation & Viva guide
│
├── templates/              # HTML Jinja templates
│   ├── base.html           # Layout with Navigation Bar
│   ├── index.html          # Page 1: Home
│   ├── movies.html         # Page 2: Movies (MySQL)
│   ├── book.html           # Page 3: Book Ticket (Form & Price Calculation)
│   ├── bookings.html       # Page 4: Bookings (MySQL CRUD & Search)
│   └── reviews.html        # Page 5: Reviews (MongoDB)
│
├── static/                 # Static CSS & JS assets
│   ├── style.css           # Cinema dark theme CSS styling
│   └── script.js            # Live price calculator & form validation
│
└── database/
    └── movie_booking.sql   # Complete SQL schema & initial sample data
```

---

## ⚙️ Installation & Setup Instructions

### Step 1: Install Python Dependencies
Open your terminal or command prompt in the project root directory and run:
```bash
pip install -r requirements.txt
```

### Step 2: Set Up MySQL Database
1. Open **MySQL Workbench** or **MySQL Command Line**.
2. Run the SQL script located in `database/movie_booking.sql`:
   ```sql
   SOURCE c:/Users/HP/OneDrive/Desktop/samar dbms/database/movie_booking.sql;
   ```
   *(Or copy-paste the contents of `movie_booking.sql` into MySQL Workbench and execute).*
3. Verify that the `movie_booking_db` database, along with tables `movies`, `customers`, and `bookings` have been created.

### Step 3: Start MongoDB Service
Ensure **MongoDB Community Server** is running on `localhost:27017` (default port).
- If using MongoDB service on Windows, ensure it is started in Services (`services.msc`).
- Or run `mongod` from Command Prompt.

### Step 4: Configure Database Credentials (Optional)
If your MySQL password is not empty or if your port differs, update `config.py`:
```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_mysql_password'
MYSQL_DB = 'movie_booking_db'
MYSQL_PORT = 3306

MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DB = 'movie_booking_nosql'
```

### Step 5: Launch the Application
Run the Flask server:
```bash
python app.py
```
Open your browser and navigate to:
👉 **`http://127.0.0.1:5000`**

---

## 🎯 5-Minute DBMS Viva Demonstration Flow

Follow these exact steps during your 5-minute project demonstration:

1. **Open Home Page:** Go to `http://127.0.0.1:5000`. Show the modern cinema interface and navigation.
2. **Go to Movies:** Click on **Movies** in the navigation bar. Point out the 6 movie cards loaded from MySQL.
3. **Select a Movie:** Click the **Book Now** button on any movie (e.g., *Inception*).
4. **Book Tickets:** Fill in Customer Name (e.g., `Samar`), Email (`Samar@gmail.com`), Phone (`9876543210`), select date, show time (e.g., `4:00 PM`), 2 tickets, and Premium seat type. Point out that the total amount (**₹500**) is calculated automatically on screen.
5. **Confirm Booking:** Click **Confirm Booking**. Point out the success banner and generated **Booking ID** (e.g., `#3`).
6. **Open Bookings:** Click on **Bookings** in the navigation bar. Show the newly added booking in the table.
7. **Search & Cancel Demo:** Type `Samar` in the search box to filter. Click **Cancel Booking** to demonstrate updating the status to `Cancelled` in MySQL.
8. **Open MySQL Workbench:** Show the database tables:
   ```sql
   USE movie_booking_db;
   SELECT * FROM movies;
   SELECT * FROM customers;
   SELECT * FROM bookings;
   ```
9. **Prove SQL Storage:** Demonstrate that the customer record and booking row are stored permanently in MySQL with Foreign Key relationships.
10. **Go to Reviews:** Click on **Reviews** in the navigation bar.
11. **Submit Review:** Enter Customer Name (`Samar`), select movie (`Inception`), select 5 stars, type comment (`"Amazing background score and plot!"`), and click **Submit Review**.
12. **Show Live MongoDB Display:** Show that the review instantly appears on the page without reloads.
13. **Open MongoDB Compass / Mongo Shell:** Connect to `mongodb://localhost:27017/`.
14. **Prove NoSQL Storage:** Open database `movie_booking_nosql` -> collection `reviews`. Show the document:
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
## 📄 License & Credits
Open-source movie booking and manegement system
