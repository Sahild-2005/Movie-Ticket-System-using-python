import mysql.connector
from mysql.connector import Error
import os

# MySQL configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sahildhumal@10'  # Updated password
}

def init_database():
    conn = None
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS movie_booking")
        cursor.execute("USE movie_booking")
        
        # Drop existing tables in correct order
        cursor.execute("DROP TABLE IF EXISTS seats")
        cursor.execute("DROP TABLE IF EXISTS bookings")
        cursor.execute("DROP TABLE IF EXISTS movies")
        cursor.execute("DROP TABLE IF EXISTS users")
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                remember_me BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create movies table with image_path
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                movie_id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                duration VARCHAR(20),
                normal_price DECIMAL(10,2),
                recliner_price DECIMAL(10,2),
                image_path VARCHAR(255),
                language VARCHAR(50)
            )
        ''')
        
        # Create bookings table with user_id
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id INT AUTO_INCREMENT PRIMARY KEY,
                movie_id INT,
                user_id INT,
                customer_name VARCHAR(100),
                booking_date DATE,
                num_tickets INT,
                total_amount DECIMAL(10,2),
                FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Create seats table with seat type
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS seats (
                seat_id INT AUTO_INCREMENT PRIMARY KEY,
                booking_id INT,
                seat_number VARCHAR(10),
                is_booked BOOLEAN DEFAULT FALSE,
                seat_type ENUM('normal', 'recliner') DEFAULT 'normal',
                FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
            )
        ''')
        
        # Insert sample movies with image paths - Hindi movies with rupee prices
        sample_movies = [
            ("Animal", "3h 21m", 400.00, 800.00, "images/animal.jpg", "Hindi"),
            ("Dunki", "2h 41m", 350.00, 800.00, "images/dunki.jpg", "Hindi"),
            ("12th Fail", "2h 27m", 300.00, 800.00, "images/12th_fail.jpg", "Hindi"),
            ("Chaava", "2h 35m", 350.00, 800.00, "images/chaava.jpg", "Hindi"),
            ("Sita Ramam", "2h 42m", 350.00, 800.00, "images/sita_ramam.jpg", "Telugu"),
            ("Geeta Govindam", "2h 30m", 350.00, 800.00, "images/geeta_govindam.jpg", "Telugu"),
            ("Premalu", "2h 35m", 350.00, 800.00, "images/premalu.jpg", "Malayalam"),
            ("Kanni", "2h 30m", 350.00, 800.00, "images/kanni.jpg", "Marathi"),
            ("Kaakan", "2h 35m", 350.00, 800.00, "images/kaakan.jpg", "Marathi")
        ]
        
        cursor.executemany("""
            INSERT INTO movies (title, duration, normal_price, recliner_price, image_path, language)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, sample_movies)
            
        conn.commit()
        print("Database initialized successfully!")
        
    except Error as e:
        print(f"Error: {e}")
        
    finally:
        if conn is not None and conn.is_connected():
            cursor.close()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    init_database() 