import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create the user table
c.execute('''CREATE TABLE IF NOT EXISTS User
            (UserEmail TEXT NOT NULL PRIMARY KEY,
            UserPassword TEXT NOT NULL,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL)''')
conn.commit()

# Create the setting table
c.execute('''CREATE TABLE IF NOT EXISTS Setting
            (SettingName TEXT NOT NULL PRIMARY KEY,
            SettingValue TEXT NOT NULL,
            DefaultValue TEXT NOT NULL,
            UserEmail TEXT NOT NULL,
            FOREIGN KEY (UserEmail) REFERENCES User(UserEmail))''')
conn.commit()

# Create the game table
c.execute('''CREATE TABLE IF NOT EXISTS Game
            (GameID TEXT NOT NULL PRIMARY KEY)''')
conn.commit()

# Create the gameplay table
c.execute('''CREATE TABLE IF NOT EXISTS Gameplay
            (UserEmail TEXT NOT NULL,
            GameID TEXT NOT NULL,
            FOREIGN KEY (UserEmail) REFERENCES User(UserEmail),
            FOREIGN KEY (GameID) REFERENCES Game(GameID))''')
conn.commit()

print("Database and tables created")

# Close the connection
conn.close()