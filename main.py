import sqlite3

def show_tables(db_name="energy_data.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in database:")
    for table in tables:
        print(table[0])
    conn.close()

if __name__ == "__main__":
    show_tables()
