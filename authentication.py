import hashlib
import os
import re
import sqlite3


class authentication():
    def __init__(self, email, password):
        self.email = (email or "").strip()
        self.password = password
        self.hashed_password = hashlib.sha256(self.password.encode()).hexdigest()

    def email_check(self):
        # Simple, practical email pattern
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        # Rejects blank email inputs
        if self.email == "":
            return True, "Please enter an email"

        # Rejects email which is not in the correct format
        if not re.match(pattern, self.email):
            return True, "Invalid email format"

        # enforce max length
        if len(self.email) > 254:
            return True, "Email is too long"

        return False, ""

    # Checks if email already exists
    def email_exists(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT 1 FROM User WHERE UserEmail = ? LIMIT 1", (self.email,))
            return cursor.fetchone() is not None
        finally:
            conn.close()

    def login_func(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        try:
            # Check if email exists
            cursor.execute("SELECT UserPassword FROM User WHERE UserEmail = ?", (self.email,))
            result = cursor.fetchone()

            if not result:
                conn.close()
                return False, "Account does not exist"

            stored_hash = result[0]

            # Compare hashed passwords
            if stored_hash == self.hashed_password:
                conn.close()
                return True, "Login successful"
            else:
                conn.close()
                return False, "Incorrect password"

        except Exception as e:
            conn.close()
            return False, f"Database error: {e}"

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
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO User (UserEmail, UserPassword) VALUES (?, ?)",
                (self.email, self.hashed_password)
            )
            conn.commit()
            return False, "User registered successfully"

        except sqlite3.IntegrityError:
            return True, "Email already exists"
        finally:
            conn.close()