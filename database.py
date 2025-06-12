import sqlite3

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

# Function to display stored data from the database
def display_data():
    conn = sqlite3.connect("specimens.db")
    c = conn.cursor()
    c.execute('SELECT * FROM specimen_data')
    rows = c.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Username: {row[1]}, Microscope Size: {row[2]}, Real-Life Size: {row[3]}")
    conn.close()

# Function to calculate the real-life size
def calculate_real_life_size(microscope_size_mm, magnification):
    # Convert the size from millimeters to micrometers (1 mm = 1000 micrometers)
    microscope_size_micrometers = microscope_size_mm * 1000
    # Calculate real-life size
    return microscope_size_micrometers / magnification

# Main function
def main():
    # Create the database and table if not already created
    create_db()

    # Take user input
    username = input("Enter your username: ")
    microscope_size_mm = float(input("Enter the microscope size of the specimen (in millimeters): "))
    magnification = float(input("Enter the magnification factor: "))

    # Calculate the real-life size
    real_life_size = calculate_real_life_size(microscope_size_mm, magnification)

    # Insert the data into the database
    insert_data(username, microscope_size_mm, real_life_size)

    # Display the stored data from the database
    print("\nStored Data:")
    display_data()

if __name__ == "__main__":
    main()
