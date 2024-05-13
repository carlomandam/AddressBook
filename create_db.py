import sqlite3

def create_address_book():
    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS addresses (
                    id INTEGER PRIMARY KEY,
                    Address TEXT,
                    longitude REAL,
                    latitude REAL
                )''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_address_book()
    print("Address book database created successfully.")