import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkcalendar import DateEntry
from datetime import datetime
from PIL import Image, ImageTk
import os

# MySQL configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sahildhumal@10',
    'database': 'movie_booking'
}

class MovieBookingSystem:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Movie Ticket Booking System")
        self.root.geometry("1400x900")
        
        # Set theme and styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure custom styles
        self.style.configure("Title.TLabel", 
                           font=("Helvetica", 24, "bold"), 
                           foreground="#2c3e50",
                           padding=10)
        
        self.style.configure("MovieTitle.TLabel", 
                           font=("Helvetica", 14, "bold"), 
                           foreground="#2c3e50")
        
        self.style.configure("MovieInfo.TLabel", 
                           font=("Helvetica", 12), 
                           foreground="#34495e")
        
        self.style.configure("Price.TLabel", 
                           font=("Helvetica", 12, "bold"), 
                           foreground="#27ae60")
        
        self.style.configure("Custom.TButton", 
                           font=("Helvetica", 12),
                           padding=10,
                           background="#3498db",
                           foreground="white")
        
        self.style.configure("Selected.TButton",
                           background="#27ae60",
                           foreground="white")
        
        self.style.configure("Available.TButton",
                           background="#bdc3c7")
        
        self.style.configure("Booked.TButton",
                           background="#e74c3c")
        
        # Initialize selected_movie variable
        self.selected_movie = tk.StringVar()
        self.selected_seats = []
        
        # Database connection
        self.connect_to_database()
        
        # Create tables if they don't exist
        self.create_tables()
        
        # Create main container with padding
        self.main_container = ttk.Frame(self.root, padding="20")
        self.main_container.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights for main container
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        # Create GUI Components
        self.create_gui()
        
    def connect_to_database(self):
        try:
            self.conn = mysql.connector.connect(**MYSQL_CONFIG)
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to database: {err}")
            
    def create_tables(self):
        # Tables are now created in init_database.py
        pass
        
    def create_gui(self):
        # Create main frames with padding and borders
        self.left_frame = ttk.Frame(self.main_container, padding="20", relief="solid", borderwidth=1)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        self.right_frame = ttk.Frame(self.main_container, padding="20", relief="solid", borderwidth=1)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # Movies Section Title with custom style
        ttk.Label(self.left_frame, 
                 text="Available Movies", 
                 style="Title.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")
        
        # Create scrollable movie frame
        self.create_scrollable_movie_frame()
        
        # Booking Section
        self.create_booking_section()
        
        # History Section
        self.create_history_section()
        
    def create_scrollable_movie_frame(self):
        # Create canvas with scrollbar
        self.canvas = tk.Canvas(self.left_frame, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.left_frame, orient="vertical", command=self.canvas.yview)
        self.movie_frame = ttk.Frame(self.canvas)
        
        # Configure the canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Grid the canvas and scrollbar
        self.canvas.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        self.scrollbar.grid(row=1, column=1, sticky="ns")
        
        # Create a window in the canvas for the movie frame
        self.canvas_window = self.canvas.create_window((0, 0), window=self.movie_frame, anchor="nw")
        
        # Configure weights for scrolling
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=1)
        
        # Mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Load and display movies with images
        self.load_movies_with_images()
        
    def create_booking_section(self):
        # Booking Form Frame with custom styling
        booking_frame = ttk.LabelFrame(self.right_frame, 
                                     text="Book Your Tickets", 
                                     padding="20",
                                     style="Custom.TLabelframe")
        booking_frame.grid(row=0, column=0, pady=(0, 20), sticky="ew")
        
        # Customer Name with improved layout
        ttk.Label(booking_frame, 
                 text="Customer Name:", 
                 style="MovieInfo.TLabel").grid(row=0, column=0, pady=10, sticky="w")
        self.customer_name = ttk.Entry(booking_frame, width=30, font=("Helvetica", 12))
        self.customer_name.grid(row=0, column=1, pady=10, padx=10)
        
        # Booking Date with calendar widget
        ttk.Label(booking_frame, 
                 text="Booking Date:", 
                 style="MovieInfo.TLabel").grid(row=1, column=0, pady=10, sticky="w")
        self.booking_date = DateEntry(booking_frame, 
                                    width=20, 
                                    background='#3498db',
                                    foreground='white', 
                                    borderwidth=2,
                                    font=("Helvetica", 12))
        self.booking_date.grid(row=1, column=1, pady=10, padx=10)
        
        # Number of Tickets with spinbox
        ttk.Label(booking_frame, 
                 text="Number of Tickets:", 
                 style="MovieInfo.TLabel").grid(row=2, column=0, pady=10, sticky="w")
        self.num_tickets = ttk.Spinbox(booking_frame, 
                                     from_=1, 
                                     to=10, 
                                     width=10,
                                     font=("Helvetica", 12))
        self.num_tickets.grid(row=2, column=1, pady=10, padx=10)
        self.num_tickets.set(1)
        
        # Action Buttons with custom styling
        ttk.Button(booking_frame, 
                  text="Select Seats", 
                  command=self.show_seat_selection,
                  style="Custom.TButton").grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(booking_frame, 
                  text="Book Tickets", 
                  command=self.book_tickets,
                  style="Custom.TButton").grid(row=4, column=0, columnspan=2, pady=10)
        
    def create_history_section(self):
        # History Frame with custom styling
        history_frame = ttk.LabelFrame(self.right_frame, 
                                     text="Booking History", 
                                     padding="20",
                                     style="Custom.TLabelframe")
        history_frame.grid(row=1, column=0, pady=(20, 0), sticky="nsew")
        
        # Configure Treeview style
        self.style.configure("Treeview",
                           font=("Helvetica", 11),
                           rowheight=25)
        self.style.configure("Treeview.Heading",
                           font=("Helvetica", 12, "bold"))
        
        # Create Treeview with custom styling
        self.tree = ttk.Treeview(history_frame,
                                columns=("ID", "Movie", "Customer", "Date", "Tickets", "Seats", "Amount"),
                                show="headings",
                                height=8)
        
        # Add scrollbar to treeview
        history_scroll = ttk.Scrollbar(history_frame, orient="vertical", command=self.tree.yview)
        history_scroll.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=history_scroll.set)
        
        # Configure columns
        self.tree.heading("ID", text="Booking ID")
        self.tree.heading("Movie", text="Movie")
        self.tree.heading("Customer", text="Customer")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Tickets", text="Tickets")
        self.tree.heading("Seats", text="Seats")
        self.tree.heading("Amount", text="Amount")
        
        # Set column widths
        self.tree.column("ID", width=80)
        self.tree.column("Movie", width=150)
        self.tree.column("Customer", width=120)
        self.tree.column("Date", width=100)
        self.tree.column("Tickets", width=60)
        self.tree.column("Seats", width=100)
        self.tree.column("Amount", width=80)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # Load booking history
        self.load_booking_history()
        
        # Logout Button with custom styling
        ttk.Button(self.right_frame, 
                  text="Logout", 
                  command=self.logout,
                  style="Custom.TButton").grid(row=2, column=0, pady=20)
        
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
    def on_frame_configure(self, event=None):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def on_canvas_configure(self, event):
        """When canvas is resized, resize the inner frame to match"""
        width = event.width - 5  # Subtract a bit for the scrollbar
        self.canvas.itemconfig(self.canvas_window, width=width)
        
    def load_movies_with_images(self):
        try:
            self.cursor.execute("""
                SELECT movie_id, title, image_path, normal_price, recliner_price, language, duration 
                FROM movies
            """)
            movies = self.cursor.fetchall()
            
            # Store movie prices
            self.movie_prices = {str(movie[0]): {'normal': movie[3], 'recliner': movie[4]} 
                               for movie in movies}
            
            # Configure canvas minimum size
            self.canvas.configure(width=600, height=600)
            
            for i, (movie_id, title, image_path, normal_price, recliner_price, language, duration) in enumerate(movies):
                # Create frame for each movie with border and padding
                movie_frame = ttk.Frame(self.movie_frame, padding=15, relief="solid", borderwidth=1)
                movie_frame.grid(row=i//2, column=i%2, pady=10, padx=10, sticky="nsew")
                
                try:
                    # Get absolute path to image
                    abs_image_path = os.path.abspath(image_path)
                    
                    if not os.path.exists(abs_image_path):
                        raise FileNotFoundError(f"Image file not found: {abs_image_path}")
                    
                    image = Image.open(abs_image_path)
                    image = image.resize((200, 300), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    
                    # Create label with image
                    image_label = ttk.Label(movie_frame, image=photo)
                    image_label.image = photo
                    image_label.grid(row=0, column=0, padx=5)
                    
                except Exception as e:
                    print(f"Error loading image for {title}: {str(e)}")
                    # Fallback to text-only display
                    ttk.Label(movie_frame, 
                            text=f"[Image Not Found]\n{title}",
                            style="MovieTitle.TLabel").grid(row=0, column=0)
                
                # Movie details frame with improved styling
                details_frame = ttk.Frame(movie_frame, padding=10)
                details_frame.grid(row=1, column=0, pady=5)
                
                # Movie title and details with custom styles
                ttk.Label(details_frame, 
                         text=title,
                         style="MovieTitle.TLabel").grid(row=0, column=0, pady=(0, 5))
                
                ttk.Label(details_frame, 
                         text=f"Language: {language}",
                         style="MovieInfo.TLabel").grid(row=1, column=0, pady=2)
                
                ttk.Label(details_frame, 
                         text=f"Duration: {duration}",
                         style="MovieInfo.TLabel").grid(row=2, column=0, pady=2)
                
                ttk.Label(details_frame, 
                         text=f"Normal: ₹{normal_price:.2f}",
                         style="Price.TLabel").grid(row=3, column=0, pady=2)
                
                ttk.Label(details_frame, 
                         text=f"Recliner: ₹{recliner_price:.2f}",
                         style="Price.TLabel").grid(row=4, column=0, pady=2)
                
                # Radio button with custom style
                ttk.Radiobutton(details_frame, 
                              text="Select Movie",
                              value=str(movie_id),
                              variable=self.selected_movie,
                              style="Custom.TRadiobutton").grid(row=5, column=0, pady=5)
            
            # Update scroll region
            self.movie_frame.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
            # Configure movie frame columns
            self.movie_frame.grid_columnconfigure(0, weight=1)
            self.movie_frame.grid_columnconfigure(1, weight=1)
                    
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error loading movies: {err}")
            
    def load_booking_history(self):
        try:
            self.tree.delete(*self.tree.get_children())
            self.cursor.execute("""
                SELECT b.booking_id, m.title, b.customer_name, b.booking_date, 
                       b.num_tickets, b.total_amount,
                       GROUP_CONCAT(s.seat_number) as seats
                FROM bookings b
                JOIN movies m ON b.movie_id = m.movie_id
                LEFT JOIN seats s ON b.booking_id = s.booking_id
                WHERE b.user_id = %s
                GROUP BY b.booking_id
                ORDER BY b.booking_date DESC
            """, (self.user_id,))
            bookings = self.cursor.fetchall()
            for booking in bookings:
                # Format the date
                booking_date = booking[3].strftime('%Y-%m-%d')
                # Format the amount
                amount = f"${booking[5]:.2f}"
                # Get seats
                seats = booking[6] if booking[6] else "N/A"
                # Create the values tuple with formatted data
                values = (booking[0], booking[1], booking[2], booking_date, booking[4], seats, amount)
                self.tree.insert("", "end", values=values)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error loading booking history: {err}")
            
    def show_seat_selection(self):
        if not self.selected_movie.get():
            messagebox.showerror("Error", "Please select a movie first")
            return
            
        # Create a new window for seat selection
        seat_window = tk.Toplevel(self.root)
        seat_window.title("Select Seats")
        seat_window.geometry("800x600")
        
        # Create seat selection frame
        seat_frame = ttk.Frame(seat_window, padding="20")
        seat_frame.grid(row=0, column=0, sticky="nsew")
        
        # Screen representation
        screen_label = ttk.Label(seat_frame, text="SCREEN", font=("Helvetica", 12, "bold"))
        screen_label.grid(row=0, column=0, columnspan=10, pady=20)
        
        # Add a separator line below the screen
        separator = ttk.Separator(seat_frame, orient="horizontal")
        separator.grid(row=1, column=0, columnspan=10, sticky="ew", pady=10)
        
        # Create seat buttons
        self.selected_seats = []  # Reset selected seats
        num_tickets = int(self.num_tickets.get())
        
        # Create recliner seats (2 rows x 10 columns)
        ttk.Label(seat_frame, text="RECLINER", font=("Helvetica", 10, "bold")).grid(row=2, column=0, columnspan=10)
        for row in range(2):
            for col in range(10):
                seat_number = f"R{row+1}{col+1}"  # R11, R12, etc. for recliner seats
                seat_btn = ttk.Button(seat_frame, text=seat_number, width=5,
                                    style="Available.TButton")
                seat_btn.configure(command=lambda s=seat_number, b=seat_btn, t='recliner': 
                                 self.toggle_seat(s, b, num_tickets, t))
                seat_btn.grid(row=row+3, column=col, padx=2, pady=2)
                
                # Check if seat is already booked
                self.cursor.execute("""
                    SELECT s.seat_number 
                    FROM seats s 
                    JOIN bookings b ON s.booking_id = b.booking_id 
                    WHERE b.movie_id = %s AND s.is_booked = TRUE AND s.seat_type = 'recliner'
                """, (self.selected_movie.get(),))
                booked_seats = [seat[0] for seat in self.cursor.fetchall()]
                
                if seat_number in booked_seats:
                    seat_btn.state(['disabled'])
                    seat_btn.configure(text="X")
        
        # Add spacing between recliner and normal seats
        ttk.Label(seat_frame, text="").grid(row=5, column=0, pady=20)
        
        # Create normal seats (5 rows x 10 columns)
        ttk.Label(seat_frame, text="NORMAL", font=("Helvetica", 10, "bold")).grid(row=6, column=0, columnspan=10)
        for row in range(5):
            for col in range(10):
                seat_number = f"{chr(65+row)}{col+1}"  # A1, A2, B1, B2, etc.
                seat_btn = ttk.Button(seat_frame, text=seat_number, width=5,
                                    style="Available.TButton")
                seat_btn.configure(command=lambda s=seat_number, b=seat_btn, t='normal': 
                                 self.toggle_seat(s, b, num_tickets, t))
                seat_btn.grid(row=row+7, column=col, padx=2, pady=2)
                
                # Check if seat is already booked
                self.cursor.execute("""
                    SELECT s.seat_number 
                    FROM seats s 
                    JOIN bookings b ON s.booking_id = b.booking_id 
                    WHERE b.movie_id = %s AND s.is_booked = TRUE AND s.seat_type = 'normal'
                """, (self.selected_movie.get(),))
                booked_seats = [seat[0] for seat in self.cursor.fetchall()]
                
                if seat_number in booked_seats:
                    seat_btn.state(['disabled'])
                    seat_btn.configure(text="X")
        
        # Add legend
        legend_frame = ttk.Frame(seat_frame)
        legend_frame.grid(row=12, column=0, columnspan=10, pady=10)
        
        ttk.Label(legend_frame, text="Available", style="Available.TButton").grid(row=0, column=0, padx=5)
        ttk.Label(legend_frame, text="Selected", style="Selected.TButton").grid(row=0, column=1, padx=5)
        ttk.Label(legend_frame, text="Booked (X)").grid(row=0, column=2, padx=5)
        
        # Price information
        movie_prices = self.movie_prices[self.selected_movie.get()]
        price_frame = ttk.Frame(seat_frame)
        price_frame.grid(row=13, column=0, columnspan=10, pady=10)
        ttk.Label(price_frame, text=f"Normal: ₹{movie_prices['normal']:.2f}", font=("Helvetica", 10)).grid(row=0, column=0, padx=10)
        ttk.Label(price_frame, text=f"Recliner: ₹{movie_prices['recliner']:.2f}", font=("Helvetica", 10)).grid(row=0, column=1, padx=10)
        
        # Confirm button
        ttk.Button(seat_frame, text="Confirm Selection", 
                  command=lambda: self.confirm_seat_selection(seat_window)).grid(row=14, column=0, columnspan=10, pady=20)
        
    def toggle_seat(self, seat_number, button, max_seats, seat_type):
        if seat_number in self.selected_seats:
            self.selected_seats.remove(seat_number)
            button.configure(style="Available.TButton")
        else:
            if len(self.selected_seats) < max_seats:
                self.selected_seats.append(seat_number)
                button.configure(style="Selected.TButton")
            else:
                messagebox.showwarning("Warning", f"You can only select {max_seats} seats")
                
    def confirm_seat_selection(self, seat_window):
        if not self.selected_seats:
            messagebox.showerror("Error", "Please select at least one seat")
            return
        seat_window.destroy()
        
    def book_tickets(self):
        try:
            # Get selected movie
            selected_movie = self.selected_movie.get()
            
            if not selected_movie:
                messagebox.showerror("Error", "Please select a movie")
                return
                
            # Validate customer name
            customer_name = self.customer_name.get().strip()
            if not customer_name:
                messagebox.showerror("Error", "Please enter customer name")
                return
            
            # Get number of tickets
            try:
                num_tickets = int(self.num_tickets.get())
                if num_tickets < 1:
                    raise ValueError("Invalid number of tickets")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number of tickets")
                return
                
            # Validate seat selection
            if not self.selected_seats:
                messagebox.showerror("Error", "Please select seats")
                return
                
            if len(self.selected_seats) != num_tickets:
                messagebox.showerror("Error", f"Please select exactly {num_tickets} seats")
                return
            
            # Calculate total amount
            movie_prices = self.movie_prices.get(selected_movie)
            total_amount = 0
            for seat in self.selected_seats:
                if seat.startswith('R'):  # Recliner seat
                    total_amount += movie_prices['recliner']
                else:  # Normal seat
                    total_amount += movie_prices['normal']
            
            # Insert booking
            self.cursor.execute("""
                INSERT INTO bookings (movie_id, user_id, customer_name, booking_date, num_tickets, total_amount)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (selected_movie, self.user_id, customer_name, self.booking_date.get_date(),
                  num_tickets, total_amount))
            
            # Get the booking ID
            booking_id = self.cursor.lastrowid
            
            # Insert seats
            for seat_number in self.selected_seats:
                seat_type = 'recliner' if seat_number.startswith('R') else 'normal'
                self.cursor.execute("""
                    INSERT INTO seats (booking_id, seat_number, is_booked, seat_type)
                    VALUES (%s, %s, TRUE, %s)
                """, (booking_id, seat_number, seat_type))
            
            self.conn.commit()
            
            messagebox.showinfo("Success", 
                              f"Booking successful!\nSeats: {', '.join(self.selected_seats)}\nTotal Amount: ₹{total_amount:.2f}")
            self.load_booking_history()
            
            # Clear fields
            self.customer_name.delete(0, tk.END)
            self.num_tickets.delete(0, tk.END)
            self.num_tickets.insert(0, "1")
            self.selected_movie.set("")  # Clear movie selection
            self.selected_seats = []  # Clear selected seats
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error booking tickets: {err}")
            
    def logout(self):
        self.root.destroy()
        from auth import AuthSystem
        auth = AuthSystem()
        auth.run()

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieBookingSystem(root, 1)  # Default user_id for testing
    root.mainloop() 