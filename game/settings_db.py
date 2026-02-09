import sqlite3

DB = "database.db"

DEFAULT_BG = "Blue.png"

def set_background(user_email: str, bg_filename: str):
    if not user_email:
        return
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON;")
    c = conn.cursor()

    c.execute("""
        INSERT INTO UserSetting (UserEmail, SettingName, SettingValue)
        VALUES (?, 'background', ?)
        ON CONFLICT(UserEmail, SettingName) DO UPDATE SET SettingValue=excluded.SettingValue
    """, (user_email, bg_filename))

    conn.commit()
    conn.close()

def get_background(user_email: str) -> str:
    if not user_email:
        return DEFAULT_BG

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
        SELECT SettingValue
        FROM UserSetting
        WHERE UserEmail = ? AND SettingName = 'background'
        LIMIT 1
    """, (user_email,))
    row = c.fetchone()
    conn.close()

    return row[0] if row else DEFAULT_BG