import sqlite3
from faker import Faker

# Create a new SQLite database (or connect to an existing one)
conn = sqlite3.connect('fake_users.db')
cursor = conn.cursor()

# Create a table for user data
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    address TEXT,
    phone TEXT,
    date_of_birth TEXT
)
''')

# Initialize Faker
fake = Faker()

# Generate and insert 100 fake user entries
for _ in range(100):
    name = fake.name()
    email = fake.email()
    address = fake.address().replace('\n', ', ')
    phone = fake.phone_number()
    date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat()

    cursor.execute('''
    INSERT INTO users (name, email, address, phone, date_of_birth)
    VALUES (?, ?, ?, ?, ?)
    ''', (name, email, address, phone, date_of_birth))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database 'fake_users.db' created with 100 fake user entries.")
