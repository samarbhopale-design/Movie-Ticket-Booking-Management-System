import os

class Config:
    """
    Database Configuration for MySQL and MongoDB.
    Modify host, user, password, and port according to your local installation.
    """
    # MySQL Database Settings
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'Sujal@123')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'movie_booking_db')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))

    # MongoDB Settings
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
    MONGO_DB = os.environ.get('MONGO_DB', 'movie_booking_nosql')
    MONGO_COLLECTION = 'reviews'

    # Secret key for Flask Flash messages
    SECRET_KEY = os.environ.get('SECRET_KEY', 'college_dbms_project_secret_key_2026')
