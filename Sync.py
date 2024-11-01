import os
import requests
import sqlite3
import base64
import re

# Database ID
DBID = "97065"
# Super Token
Token = "90225A9B19414979BE70DCEDFBCE6E6C"
################################################-DEVICE TABLE-#####################################################################
# Endpoint URL
Device_url = f'https://appnostic.dbflex.net/secure/api/v2/{DBID}/{Token}/ZK%20Device/select.json'
# Fetch JSON data from the endpoint
Device_response = requests.get(Device_url)
data = Device_response.json()

# Debugging: Print the fetched data
print("Fetched data:", data)

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('PUSH.db')
cursor = conn.cursor()

# Create table if it doesn't exist
table_name = 'DEVICES'
cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, remote_id INTEGER)')

# Function to check if a column exists
def Column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [info[1] for info in cursor.fetchall()]
    return column_name in columns

# Check if the column 'remote_id' exists and add it if it doesn't
if not Column_exists(cursor, table_name, 'remote_id'):
    cursor.execute(f'ALTER TABLE {table_name} ADD COLUMN remote_id INTEGER')
    conn.commit()

# Function to sanitize column names
def Sanitize_column_name(name):
    return re.sub(r'\W|^(?=\d)', '_', name)

# Add new columns if they don't exist
for key in data[0].keys():
    if key == 'Id':  # Skip the 'Id' key
        continue
    sanitized_key = Sanitize_column_name(key)
    if not Column_exists(cursor, table_name, sanitized_key):
        cursor.execute(f'ALTER TABLE {table_name} ADD COLUMN {sanitized_key} TEXT')

# Insert data into the table
for item in data:
    sanitized_item = {Sanitize_column_name(k): v for k, v in item.items() if k != 'Id'}
    sanitized_item['remote_id'] = item['Id']  # Add 'remote_id' with the value of 'Id'
    columns = ', '.join(sanitized_item.keys())
    placeholders = ', '.join(['?' for _ in sanitized_item])
    insert_query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
    cursor.execute(insert_query, list(sanitized_item.values()))

# Commit changes and close the connection
conn.commit()
conn.close()

print("DEVICES UPDATED.")