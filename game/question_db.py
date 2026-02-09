import sqlite3
import random

DB = "database.db"

def get_random_question():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT QuestionID, QuestionText, OptionA, OptionB, OptionC, OptionD, CorrectOption
        FROM Question
    """)
    rows = c.fetchall()
    conn.close()

    if not rows:
        return None

    q = random.choice(rows)
    return {
        "id": q[0],
        "text": q[1],
        "A": q[2],
        "B": q[3],
        "C": q[4],
        "D": q[5],
        "correct": q[6],
    }

def record_attempt(user_email, question_id, chosen_option, is_correct):
    """
    user_email must exist in User table for FOREIGN KEY to succeed
    """
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        INSERT INTO QuestionAttempt (UserEmail, QuestionID, ChosenOption, IsCorrect)
        VALUES (?, ?, ?, ?)
    """, (user_email, question_id, chosen_option, 1 if is_correct else 0))
    conn.commit()
    conn.close()