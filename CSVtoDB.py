"""
    Description of the file - moving the csv data to the SQL database
"""

import sqlite3
import csv


def create_order_history_table():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_history (
            odate TEXT,
            ouser TEXT,
            osymbol TEXT,
            oon TEXT,
            ostatus TEXT,
            obp REAL,
            oltp REAL,
            oquantity INTEGER,
            ocon TEXT,
            ocostatus TEXT,
            ollstatus TEXT
        )
    ''')

    conn.commit()
    conn.close()


def insert_data_from_csv(csv_filename):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    with open(csv_filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            cursor.execute('''
                INSERT INTO order_history (odate, ouser, osymbol, oon, ostatus, obp, oltp, oquantity, ocon, ocostatus, ollstatus)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', row)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_order_history_table()
    insert_data_from_csv('order_history.csv')
    print("Database table 'order_history' created and populated successfully.")
