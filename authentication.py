import hashlib
import os
import re
import sqlite3


class authentication():
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.hashed_password = hashlib.sha256(self.password.encode()).hexdigest()

    def login_func(self):
        pass

    def password_check(self, re_password):

        if self.password != re_password:
            error_message = "Passwords do not match"
            return True, error_message

        if len(self.password) < 8:
            error_message = ("Password must be at least 8 characters long")
            return True, error_message

        if not re.search(r"[A-Z]", self.password):
            error_message = ("Password must contain at least one uppercase letter")
            return True, error_message

        if not re.search(r"[a-z]", self.password):
            error_message = ("Password must contain at least one lowercase letter")
            return True, error_message

        if not re.search(r"[0-9]", self.password):
            error_message = ("Password must contain at least one number")
            return True, error_message

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=/\\\[\]]", self.password):
            error_message = ("Password must contain at least one special character")
            return True, error_message

        return False, ""

    def sign_up(self):
        print("DB PATH:", os.path.abspath("database.db"))
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO User (UserEmail, UserPassword) VALUES (?, ?)",
                           (self.email, self.hashed_password))
            conn.commit()
            print("User registered successfully")

        except sqlite3.IntegrityError:
            print("Email already exists")

        conn.close()