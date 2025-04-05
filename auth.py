import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import hashlib
from movie_booking import MovieBookingSystem
import json
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class AuthSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Movie Booking System - Login")
        self.root.geometry("500x600")
        
        # Set theme and styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure custom styles
        self.style.configure("Title.TLabel", 
                           font=("Helvetica", 24, "bold"), 
                           foreground="#2c3e50",
                           padding=10)
        
        self.style.configure("Subtitle.TLabel", 
                           font=("Helvetica", 12), 
                           foreground="#34495e")
        
        self.style.configure("Custom.TButton", 
                           font=("Helvetica", 12),
                           padding=10,
                           background="#3498db",
                           foreground="white")
        
        self.style.configure("Link.TButton", 
                           font=("Helvetica", 10, "underline"),
                           foreground="#3498db",
                           background="white")
        
        # MySQL configuration
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Sahildhumal@10',
            'database': 'movie_booking'
        }
        
        # Initialize encryption key
        self.init_encryption()
        
        self.create_login_page()
        
    def init_encryption(self):
        # Create a key file if it doesn't exist
        if not os.path.exists('key.key'):
            key = Fernet.generate_key()
            with open('key.key', 'wb') as key_file:
                key_file.write(key)
        
        # Load the key
        with open('key.key', 'rb') as key_file:
            self.key = key_file.read()
        self.cipher_suite = Fernet(self.key)
        
    def save_credentials(self, username, password):
        try:
            credentials = {
                'username': username,
                'password': self.hash_password(password)
            }
            encrypted_data = self.cipher_suite.encrypt(json.dumps(credentials).encode())
            with open('credentials.enc', 'wb') as f:
                f.write(encrypted_data)
            return True
        except Exception as e:
            print(f"Error saving credentials: {e}")
            return False
            
    def load_credentials(self):
        try:
            if os.path.exists('credentials.enc'):
                with open('credentials.enc', 'rb') as f:
                    encrypted_data = f.read()
                decrypted_data = self.cipher_suite.decrypt(encrypted_data)
                credentials = json.loads(decrypted_data.decode())
                return credentials
            return None
        except Exception as e:
            print(f"Error loading credentials: {e}")
            return None
            
    def create_login_page(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Create main container with padding and border
        main_frame = ttk.Frame(self.root, padding="40")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Title with custom style
        ttk.Label(main_frame, 
                 text="Welcome Back!", 
                 style="Title.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Subtitle
        ttk.Label(main_frame, 
                 text="Please login to continue", 
                 style="Subtitle.TLabel").grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Login form with improved layout
        ttk.Label(main_frame, 
                 text="Username:", 
                 style="Subtitle.TLabel").grid(row=2, column=0, pady=10, sticky="w")
        self.username = ttk.Entry(main_frame, width=30, font=("Helvetica", 12))
        self.username.grid(row=2, column=1, pady=10, padx=10)
        
        ttk.Label(main_frame, 
                 text="Password:", 
                 style="Subtitle.TLabel").grid(row=3, column=0, pady=10, sticky="w")
        self.password = ttk.Entry(main_frame, show="*", width=30, font=("Helvetica", 12))
        self.password.grid(row=3, column=1, pady=10, padx=10)
        
        # Remember me checkbox with custom style
        self.remember_me = tk.BooleanVar()
        ttk.Checkbutton(main_frame, 
                       text="Remember Me",
                       variable=self.remember_me,
                       style="Subtitle.TCheckbutton").grid(row=4, column=0, columnspan=2, pady=10)
        
        # Action buttons with custom styling
        ttk.Button(main_frame, 
                  text="Login",
                  command=self.login,
                  style="Custom.TButton",
                  width=20).grid(row=5, column=0, columnspan=2, pady=20)
        
        # Sign up link
        ttk.Label(main_frame, 
                 text="Don't have an account?",
                 style="Subtitle.TLabel").grid(row=6, column=0, columnspan=2, pady=(20, 5))
        
        ttk.Button(main_frame, 
                  text="Sign Up",
                  command=self.create_signup_page,
                  style="Link.TButton").grid(row=7, column=0, columnspan=2)
        
    def create_signup_page(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Create main container with padding and border
        main_frame = ttk.Frame(self.root, padding="40")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Title with custom style
        ttk.Label(main_frame, 
                 text="Create Account", 
                 style="Title.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Subtitle
        ttk.Label(main_frame, 
                 text="Please fill in your details", 
                 style="Subtitle.TLabel").grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Signup form with improved layout
        ttk.Label(main_frame, 
                 text="Username:", 
                 style="Subtitle.TLabel").grid(row=2, column=0, pady=10, sticky="w")
        self.new_username = ttk.Entry(main_frame, width=30, font=("Helvetica", 12))
        self.new_username.grid(row=2, column=1, pady=10, padx=10)
        
        ttk.Label(main_frame, 
                 text="Email:", 
                 style="Subtitle.TLabel").grid(row=3, column=0, pady=10, sticky="w")
        self.email = ttk.Entry(main_frame, width=30, font=("Helvetica", 12))
        self.email.grid(row=3, column=1, pady=10, padx=10)
        
        ttk.Label(main_frame, 
                 text="Password:", 
                 style="Subtitle.TLabel").grid(row=4, column=0, pady=10, sticky="w")
        self.new_password = ttk.Entry(main_frame, show="*", width=30, font=("Helvetica", 12))
        self.new_password.grid(row=4, column=1, pady=10, padx=10)
        
        ttk.Label(main_frame, 
                 text="Confirm Password:", 
                 style="Subtitle.TLabel").grid(row=5, column=0, pady=10, sticky="w")
        self.confirm_password = ttk.Entry(main_frame, show="*", width=30, font=("Helvetica", 12))
        self.confirm_password.grid(row=5, column=1, pady=10, padx=10)
        
        # Action buttons with custom styling
        ttk.Button(main_frame, 
                  text="Sign Up",
                  command=self.signup,
                  style="Custom.TButton",
                  width=20).grid(row=6, column=0, columnspan=2, pady=20)
        
        # Login link
        ttk.Label(main_frame, 
                 text="Already have an account?",
                 style="Subtitle.TLabel").grid(row=7, column=0, columnspan=2, pady=(20, 5))
        
        ttk.Button(main_frame, 
                  text="Back to Login",
                  command=self.create_login_page,
                  style="Link.TButton").grid(row=8, column=0, columnspan=2)
        
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
        
    def login(self):
        username = self.username.get()
        password = self.password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()
            
            cursor.execute("SELECT user_id, username FROM users WHERE username = %s AND password = %s",
                         (username, self.hash_password(password)))
            user = cursor.fetchone()
            
            if user:
                # Update remember_me status
                self.update_remember_me(username, self.remember_me.get())
                
                self.root.destroy()
                root = tk.Tk()
                app = MovieBookingSystem(root, user[0])  # Pass user_id to MovieBookingSystem
                root.mainloop()
            else:
                messagebox.showerror("Error", "Invalid username or password")
                
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
                
    def signup(self):
        username = self.new_username.get()
        email = self.email.get()
        password = self.new_password.get()
        confirm = self.confirm_password.get()
        
        if not username or not email or not password or not confirm:
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
            
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()
            
            # Check if username or email already exists
            cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username or email already exists")
                return
                
            # Insert new user
            cursor.execute("""
                INSERT INTO users (username, email, password)
                VALUES (%s, %s, %s)
            """, (username, email, self.hash_password(password)))
            
            conn.commit()
            messagebox.showinfo("Success", "Account created successfully!")
            self.create_login_page()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
                
    def update_remember_me(self, username, remember_me):
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()
            
            # Update remember_me status for all users
            cursor.execute("UPDATE users SET remember_me = FALSE")
            
            # Set remember_me for the current user if checked
            if remember_me:
                cursor.execute("UPDATE users SET remember_me = TRUE WHERE username = %s", (username,))
            
            conn.commit()
            
        except mysql.connector.Error as err:
            print(f"Error updating remember_me: {err}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
                
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    auth = AuthSystem()
    auth.run() 