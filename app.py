import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error as MySQLError
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# ============================================================
# DATABASE CONNECTIONS
# ============================================================

def get_mysql_connection():
    """Establishes and returns a connection to the MySQL Database."""
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT
        )
        return connection
    except MySQLError as err:
        print(f"[MySQL Error] {err}")
        return None

def get_mongo_connection():
    """Establishes and returns a connection to MongoDB collection."""
    try:
        # Short timeout so app fails fast if MongoDB server is offline
        client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=2000)
        # Test server availability
        client.admin.command('ping')
        db = client[Config.MONGO_DB]
        collection = db[Config.MONGO_COLLECTION]
        return collection
    except PyMongoError as err:
        print(f"[MongoDB Error] {err}")
        return None

# ============================================================
# MYSQL HELPER FUNCTIONS (Movies, Customers, Bookings)
# ============================================================

def fetch_movies():
    """Fetch all movies from MySQL database."""
    conn = get_mysql_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM movies ORDER BY movie_id ASC")
        movies = cursor.fetchall()
        cursor.close()
        conn.close()
        return movies
    except MySQLError as err:
        print(f"[Error fetching movies] {err}")
        return []

def fetch_movie_by_id(movie_id):
    """Fetch single movie by ID from MySQL database."""
    conn = get_mysql_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM movies WHERE movie_id = %s", (movie_id,))
        movie = cursor.fetchone()
        cursor.close()
        conn.close()
        return movie
    except MySQLError as err:
        print(f"[Error fetching movie] {err}")
        return None

def add_booking(customer_name, email, phone, movie_id, booking_date, show_time, tickets, seat_type, total_amount):
    """
    Inserts Customer (if not already exists) and creates Booking in MySQL.
    Returns (success_boolean, booking_id_or_error_message).
    """
    conn = get_mysql_connection()
    if not conn:
        return False, "Database connection error! Check if MySQL server is running."

    try:
        cursor = conn.cursor(dictionary=True)
        
        # Check if customer already exists by email or phone
        cursor.execute("SELECT customer_id FROM customers WHERE email = %s OR phone = %s", (email, phone))
        existing_customer = cursor.fetchone()
        
        if existing_customer:
            customer_id = existing_customer['customer_id']
        else:
            # Insert new customer
            cursor.execute(
                "INSERT INTO customers (customer_name, email, phone) VALUES (%s, %s, %s)",
                (customer_name, email, phone)
            )
            customer_id = cursor.lastrowid
        
        # Insert Booking
        cursor.execute(
            """
            INSERT INTO bookings (customer_id, movie_id, booking_date, show_time, tickets, seat_type, total_amount, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'Confirmed')
            """,
            (customer_id, movie_id, booking_date, show_time, tickets, seat_type, total_amount)
        )
        booking_id = cursor.lastrowid
        
        conn.commit()
        cursor.close()
        conn.close()
        return True, booking_id
    except MySQLError as err:
        print(f"[Error adding booking] {err}")
        return False, f"Database error: {str(err)}"

def fetch_bookings(search_query=None):
    """
    Fetch all bookings joined with Customer & Movie details.
    Supports search by Customer Name or Booking ID.
    """
    conn = get_mysql_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT 
                b.booking_id,
                c.customer_name,
                c.email,
                c.phone,
                m.movie_name,
                b.booking_date,
                b.show_time,
                b.tickets,
                b.seat_type,
                b.total_amount,
                b.status
            FROM bookings b
            JOIN customers c ON b.customer_id = c.customer_id
            JOIN movies m ON b.movie_id = m.movie_id
        """
        params = []
        if search_query:
            search_query = search_query.strip()
            # Search by booking_id if numeric, else search customer name
            if search_query.isdigit():
                sql += " WHERE b.booking_id = %s "
                params.append(int(search_query))
            else:
                sql += " WHERE c.customer_name LIKE %s OR m.movie_name LIKE %s "
                params.extend([f"%{search_query}%", f"%{search_query}%"])
        
        sql += " ORDER BY b.booking_id DESC"
        cursor.execute(sql, params)
        bookings = cursor.fetchall()
        cursor.close()
        conn.close()
        return bookings
    except MySQLError as err:
        print(f"[Error fetching bookings] {err}")
        return []

def cancel_booking(booking_id):
    """Updates booking status to 'Cancelled' in MySQL."""
    conn = get_mysql_connection()
    if not conn:
        return False, "Database connection error! Check if MySQL server is running."

    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE bookings SET status = 'Cancelled' WHERE booking_id = %s", (booking_id,))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        if affected > 0:
            return True, "Booking cancelled successfully!"
        else:
            return False, "Booking ID not found."
    except MySQLError as err:
        print(f"[Error cancelling booking] {err}")
        return False, f"Database error: {str(err)}"

# ============================================================
# MONGODB HELPER FUNCTIONS (Movie Reviews)
# ============================================================

def add_review(customer_name, movie_name, rating, comment):
    """Inserts a movie review document into MongoDB."""
    collection = get_mongo_connection()
    if collection is None:
        return False, "MongoDB connection error! Please ensure MongoDB is running on localhost:27017."

    try:
        doc = {
            "customer_name": customer_name,
            "movie_name": movie_name,
            "rating": int(rating),
            "comment": comment,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        collection.insert_one(doc)
        return True, "Review submitted successfully to MongoDB!"
    except PyMongoError as err:
        print(f"[MongoDB insert error] {err}")
        return False, f"MongoDB error: {str(err)}"

def fetch_reviews():
    """Fetches all review documents from MongoDB."""
    collection = get_mongo_connection()
    if collection is None:
        return []

    try:
        # Fetch reviews sorted by newest first
        reviews = list(collection.find({}, {'_id': 0}).sort('_id', -1))
        return reviews
    except PyMongoError as err:
        print(f"[MongoDB fetch error] {err}")
        return []

# ============================================================
# FLASK ROUTES
# ============================================================

@app.route('/')
def index():
    """Page 1: Home Page"""
    return render_template('index.html')

@app.route('/movies')
def movies():
    """Page 2: Movies Page"""
    movie_list = fetch_movies()
    db_error = (get_mysql_connection() is None)
    return render_template('movies.html', movies=movie_list, db_error=db_error)

@app.route('/book', methods=['GET', 'POST'])
def book():
    """Page 3: Book Ticket Page (Form & Processing)"""
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        movie_id = request.form.get('movie_id', '')
        booking_date = request.form.get('booking_date', '')
        show_time = request.form.get('show_time', '')
        tickets_str = request.form.get('tickets', '1')
        seat_type = request.form.get('seat_type', 'Regular')

        # Validation
        if not customer_name or not email or not phone or not movie_id or not booking_date or not show_time:
            flash("All form fields are required!", "danger")
            return redirect(url_for('book'))

        try:
            tickets = int(tickets_str)
            if tickets <= 0:
                flash("Ticket quantity must be at least 1!", "warning")
                return redirect(url_for('book'))
        except ValueError:
            flash("Invalid ticket quantity!", "warning")
            return redirect(url_for('book'))

        # Calculate Total Amount
        # Regular = 150 per ticket, Premium = 250 per ticket
        price_per_ticket = 250 if seat_type == 'Premium' else 150
        total_amount = tickets * price_per_ticket

        # Save to MySQL
        success, result = add_booking(
            customer_name, email, phone, movie_id,
            booking_date, show_time, tickets, seat_type, total_amount
        )

        if success:
            booking_id = result
            flash(f"🎉 Booking Confirmed! Your Booking ID is #{booking_id}. Total Paid: ₹{total_amount}", "success")
            return redirect(url_for('bookings'))
        else:
            flash(result, "danger")
            return redirect(url_for('book'))

    # GET request
    selected_movie_id = request.args.get('movie_id', None)
    movie_list = fetch_movies()
    db_error = (get_mysql_connection() is None)
    today_date = datetime.date.today().strftime('%Y-%m-%d')
    return render_template(
        'book.html',
        movies=movie_list,
        selected_movie_id=selected_movie_id,
        today_date=today_date,
        db_error=db_error
    )

@app.route('/bookings')
def bookings():
    """Page 4: Manage Bookings Page"""
    search_query = request.args.get('search', '').strip()
    booking_list = fetch_bookings(search_query)
    db_error = (get_mysql_connection() is None)
    return render_template('bookings.html', bookings=booking_list, search_query=search_query, db_error=db_error)

@app.route('/cancel/<int:booking_id>', methods=['POST', 'GET'])
def cancel(booking_id):
    """Cancel Booking Action"""
    success, message = cancel_booking(booking_id)
    if success:
        flash(f"Booking #{booking_id} has been cancelled.", "warning")
    else:
        flash(message, "danger")
    return redirect(url_for('bookings'))

@app.route('/reviews')
def reviews():
    """Page 5: Reviews Page (MongoDB)"""
    review_list = fetch_reviews()
    movie_list = fetch_movies()
    mongo_error = (get_mongo_connection() is None)
    return render_template('reviews.html', reviews=review_list, movies=movie_list, mongo_error=mongo_error)

@app.route('/add_review', methods=['POST'])
def add_review_route():
    """Handle Review Submission to MongoDB"""
    customer_name = request.form.get('customer_name', '').strip()
    movie_name = request.form.get('movie_name', '').strip()
    rating = request.form.get('rating', '5')
    comment = request.form.get('comment', '').strip()

    if not customer_name or not movie_name or not comment:
        flash("Please complete all review fields!", "warning")
        return redirect(url_for('reviews'))

    success, message = add_review(customer_name, movie_name, rating, comment)
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")

    return redirect(url_for('reviews'))

# ============================================================
# MAIN APPLICATION RUNNER
# ============================================================

if __name__ == '__main__':
    print("=====================================================")
    print(" 🎬 Movie Ticket Booking & Management System Running ")
    print(" Flask Server: http://127.0.0.1:5000 ")
    print(" DBMS Project: MySQL (Bookings) + MongoDB (Reviews) ")
    print("=====================================================")
    app.run(debug=True, port=5000)
