from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Used for flashing messages

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

# Function to calculate the real-life size (convert from mm to µm)
def calculate_real_life_size(microscope_size, magnification):
    # Convert mm to micrometers (1 mm = 1000 µm)
    microscope_size_in_um = microscope_size * 1000
    # Now, calculate the real life size using magnification
    return microscope_size_in_um / magnification

# Function to get all stored data
def get_all_data():
    conn = sqlite3.connect("specimens.db")
    c = conn.cursor()
    c.execute('SELECT * FROM specimen_data')
    rows = c.fetchall()
    conn.close()
    return rows

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    username = request.form['username']
    microscope_size = request.form['microscope_size']
    magnification = request.form['magnification']

    try:
        microscope_size = float(microscope_size)
        magnification = float(magnification)
        real_life_size = calculate_real_life_size(microscope_size, magnification)

        # Insert data into the database
        insert_data(username, microscope_size, real_life_size)

        flash(f"Real-life size: {real_life_size:.2f} micrometers", 'success')
        return redirect(url_for('index'))

    except ValueError:
        flash("Please enter valid numbers for size and magnification.", 'error')
        return redirect(url_for('index'))

@app.route('/view_data')
def view_data():
    rows = get_all_data()
    return render_template('view_data.html', rows=rows)

if __name__ == "__main__":
    create_db()  # Create the database and table if not already created
    app.run(debug=True)
