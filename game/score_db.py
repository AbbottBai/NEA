import sqlite3

DB = "database.db"

def submit_score(user_email: str, score: int):
    """
    Updates the user's HighScore if the new score is higher.
    Creates row if it doesn't exist.
    """
    if not user_email:
        return  # avoid crashing if somehow None

    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON;")
    c = conn.cursor()

    # Ensure a row exists
    c.execute("""
        INSERT OR IGNORE INTO Score (UserEmail, HighScore)
        VALUES (?, 0)
    """, (user_email,))

    # Update only if score is higher
    c.execute("""
        UPDATE Score
        SET HighScore = ?
        WHERE UserEmail = ? AND ? > HighScore
    """, (score, user_email, score))

    conn.commit()
    conn.close()

def get_top_scores(limit: int = 5):
    """
    Returns list of dicts like: [{"name": email, "score": highscore}, ...]
    """
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
        SELECT UserEmail, HighScore
        FROM Score
        ORDER BY HighScore DESC
        LIMIT ?
    """, (limit,))

    rows = c.fetchall()
    conn.close()

    return [{"name": email, "score": highscore} for (email, highscore) in rows]