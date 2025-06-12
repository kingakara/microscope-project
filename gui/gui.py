import tkinter as tk
from tkinter import messagebox
import sqlite3


def CalrealLifeSize(microscope_size, magnification):
    microscope_size_um = microscope_size * 1000

    # Formula to calculate the real-life size in micrometers
    real_life_size_um = microscope_size_um / magnification
    return real_life_size_um

# Function to create a database and table if it doesn't exist
def create_db():
    conn = sqlite3.connect("specimens.db")
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS specimen_data (
        id INTEGER PRIMARY KEY,
        username TEXT,
        microscope_size REAL,
        real_life_size REAL
    )''')
    conn.commit()
    conn.close()

# Function to insert data into the database
def insert_data(username, microscope_size, real_life_size):
    conn = sqlite3.connect("specimens.db")
    c = conn.cursor()
    c.execute('''
    INSERT INTO specimen_data (username, microscope_size, real_life_size)
    VALUES (?, ?, ?)
    ''', (username, microscope_size, real_life_size))
    conn.commit()
    conn.close()


# Function to display stored data
def display_data():
    conn = sqlite3.connect("specimens.db")
    c = conn.cursor()
    c.execute('SELECT * FROM specimen_data')
    rows = c.fetchall()
    conn.close()
    return rows

# Function to handle the calculation and saving
def calculate_and_save():
    username = entry_username.get()
    try:
        microscope_size = float(entry_microscope_size.get())
        magnification = float(entry_magnification.get())
        real_life_size = CalrealLifeSize(microscope_size, magnification)

        # Insert data into the database
        insert_data(username, microscope_size, real_life_size)

        # Display result
        label_result.config(text=f"Real-life size: {real_life_size:.2f} micrometers")
        messagebox.showinfo("Success", "Data has been saved!")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for size and magnification.")

# Function to show stored data
def show_stored_data():
    rows = display_data()
    stored_data_window = tk.Toplevel(window)
    stored_data_window.title("Stored Data")

    for i, row in enumerate(rows):
        tk.Label(stored_data_window, text=f"ID: {row[0]} | Username: {row[1]} | Microscope Size: {row[2]} | Real-Life Size: {row[3]}").pack()

# Create the main window
window = tk.Tk()
window.title("Specimen Size Calculator")

# Create the database and table if not already created
create_db()

# Labels and input fields
label_username = tk.Label(window, text="Enter your username:")
label_username.pack()
entry_username = tk.Entry(window)
entry_username.pack()

label_microscope_size = tk.Label(window, text="Enter the microscope size (in micrometers):")
label_microscope_size.pack()
entry_microscope_size = tk.Entry(window)
entry_microscope_size.pack()

label_magnification = tk.Label(window, text="Enter the magnification factor:")
label_magnification.pack()
entry_magnification = tk.Entry(window)
entry_magnification.pack()

# Button to calculate and save data
button_calculate = tk.Button(window, text="Calculate and Save", command=calculate_and_save)
button_calculate.pack()

# Label to display the real-life size result
label_result = tk.Label(window, text="Real-life size: ")
label_result.pack()

# Button to show stored data
button_show_data = tk.Button(window, text="Show Stored Data", command=show_stored_data)
button_show_data.pack()

# Start the GUI event loop
window.mainloop()
