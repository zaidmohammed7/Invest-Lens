"""
    Description of the file - validate and interact with users and their data
"""

import re
import sqlite3
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def init_db():
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS credentials (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id TEXT UNIQUE NOT NULL,
                            hashed_password TEXT NOT NULL)''')
        conn.commit()

def validate_password(password):
    """Validate the password for complexity."""
    if (len(password) < 8 or
        not any(char.isupper() for char in password) or
        not any(char.islower() for char in password) or
        not any(char.isdigit() for char in password) or
        not any(char in "#$^" for char in password) or
        any(char in '!"%&\'()*+,-./:;<=>?@[\\]_`{|}~' for char in password)):
        return False
    return True

def validate_user_id(user_id):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    phone_regex = r'^\+?\d{10,15}$'
    return re.match(email_regex, user_id) or re.match(phone_regex, user_id)

def add_user(user_id, password):
    if not validate_user_id(user_id):
        print("Invalid User ID. It must be a valid email or phone number.")
        return
    if not validate_password(password):
        print("Invalid Password. It must be at least 8 characters, contain mixed case, numbers, and one of the following special characters: #$^")
        return

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO credentials (user_id, hashed_password) VALUES (?, ?)", (user_id, hashed_password))
            conn.commit()
            print(f"User {user_id} added successfully.")
        except sqlite3.IntegrityError:
            print(f"User {user_id} already exists.")

def remove_user(user_id):
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM credentials WHERE user_id = ?", (user_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"User {user_id} removed successfully.")
        else:
            print(f"User {user_id} does not exist.")

def reset_password(user_id, new_password):
    if not validate_password(new_password):
        print("Invalid Password. It must be at least 8 characters, contain mixed case, numbers, and one of the following special characters: #$^")
        return

    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE credentials SET hashed_password = ? WHERE user_id = ?", (hashed_password, user_id))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Password for {user_id} has been reset.")
        else:
            print(f"User {user_id} does not exist.")

def view_users():
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, user_id FROM credentials")
        credentials = cursor.fetchall()
        if credentials:
            print("\nRegistered credentials:")
            for user in credentials:
                print(f"ID: {user[0]}, User ID: {user[1]}")
        else:
            print("\nNo users found in the database.")

def main():
    init_db()
    while True:
        print("\nUser Management System")
        print("1. Add User")
        print("2. Remove User")
        print("3. Reset Password")
        print("4. View Users")
        print("5. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            user_id = input("Enter User ID (email or phone): ")
            password = input("Enter Password: ")
            add_user(user_id, password)
        elif choice == '2':
            user_id = input("Enter User ID to remove: ")
            remove_user(user_id)
        elif choice == '3':
            user_id = input("Enter User ID to reset password: ")
            new_password = input("Enter New Password: ")
            reset_password(user_id, new_password)
        elif choice == '4':
            view_users()
        elif choice == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
