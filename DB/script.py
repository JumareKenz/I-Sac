import sqlite3

# Path to your SQL file and the desired database file
sql_file = 'timetable.sql'
db_file = 'timetable.db'

# Connect to SQLite database (this will create the file if it doesn't exist)
conn = sqlite3.connect(db_file)

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Read and execute the SQL file
with open(sql_file, 'r') as file:
    sql_script = file.read()
    cursor.executescript(sql_script)

# Commit changes and close the connection
conn.commit()
conn.close()

print(f"Database '{db_file}' created and populated successfully.")
