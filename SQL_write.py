import json
import sqlite3
import time

# Function to check if a Devrec and Timestamp combination already exists in the database
def record_exists(cursor, devrec, timestamp):
    cursor.execute('SELECT 1 FROM attendance WHERE Devrec = ? AND Timestamp = ?', (devrec, timestamp))
    return cursor.fetchone() is not None

# Function to process the attlog.json file and insert records into the database
def process_attlog_file():
    # Read the content of the attlog.json file
    with open('attlog.json', 'r') as file:
        content = json.load(file)

    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('PUSH.db')
    cursor = conn.cursor()

    # Create the attendance table if it doesn't exist with additional columns as text type
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        string TEXT NOT NULL,
        ZKID TEXT,
        Timestamp TEXT,
        InorOut TEXT,
        attype TEXT,
        Device TEXT,
        SN TEXT,
        Devrec TEXT,
        FTID TEXT,
        KEY TEXT,
        RESPONSE TEXT
    )
    ''')

    # Insert each record into the attendance table with appropriate column values
    for entry in content:
        attlog = entry['attlog']
        records = attlog.split('\n')
        for record in records:
            values = record.split('\t')
            
            # Ensure there are enough values to avoid index out of range error
            if len(values) >= 7:
                # Extract values for columns
                ZKID = values[0]  # Extract ZKID value
                Timestamp = values[1]  # Extract Timestamp value
                InorOut = values[2]  # Extract InorOut value
                attype = values[3]  # Extract attype value
                Device = values[-2]  # Extract Device value
                SN = values[-1]  # Extract Serial Number value
                Devrec = values[-3]  # Extract Devrec value

                # Check if the Devrec and Timestamp combination already exists in the database
                if not record_exists(cursor, Devrec, Timestamp):
                    cursor.execute('''
                        INSERT INTO attendance (string, ZKID, Timestamp, InorOut, attype, Device, SN, Devrec)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (record, ZKID, Timestamp, InorOut, attype, Device, SN, Devrec))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    print("Attendance Records have been successfully inserted into the PUSH.db database.")

# Run the script continuously until it is manually stopped
try:
    while True:
        process_attlog_file()
        time.sleep(10)  # Wait for 10 seconds before processing the file again
except KeyboardInterrupt:
    print("Script stopped by user.")
