import sqlite3

DB = "database.db"

QUESTIONS = [
    ("Which of these is an input device?", "Monitor", "Printer", "Keyboard", "Speaker", "C"),
    ("What does CPU stand for?", "Central Processing Unit", "Computer Personal Unit", "Central Program Utility", "Control Processing Unit", "A"),
    ("Which type of memory is volatile?", "ROM", "SSD", "RAM", "HDD", "C"),
    ("What is the main purpose of an operating system?", "Write programs", "Manage hardware and software resources", "Increase internet speed", "Store files permanently", "B"),
    ("What is a compiler?", "Converts high-level code to machine code before running", "Runs code line-by-line", "Stores data temporarily", "Encrypts files", "A"),
    ("What is an interpreter?", "Converts code to machine code before running", "Runs code line-by-line translating as it goes", "Only checks spelling errors", "Converts machine code to high-level code", "B"),
    ("Which is a benefit of using hexadecimal?", "It uses only 0 and 1", "It is easier to represent large binary values", "It is faster than RAM", "It prevents hacking", "B"),
    ("How many bits are in a byte?", "4", "8", "16", "32", "B"),
    ("What is the binary value of decimal 13?", "1101", "1011", "1110", "1001", "A"),
    ("Which of these is a lossless compression method?", "JPEG", "MP3", "PNG", "AAC", "C"),
    ("Which of these is an example of an IP address?", "255.255.255.0", "00:1A:2B:3C:4D:5E", "www.example.com", "HTTP", "A"),
    ("What does LAN stand for?", "Large Area Network", "Local Area Network", "Long Access Node", "Linked Active Network", "B"),
    ("Which protocol is used to load webpages?", "FTP", "HTTP", "SMTP", "Bluetooth", "B"),
    ("What does DNS do?", "Encrypts messages", "Translates domain names to IP addresses", "Sends emails", "Blocks viruses", "B"),
    ("Which is an example of malware?", "Firewall", "Antivirus", "Trojan", "Router", "C"),
    ("What is the purpose of a firewall?", "Speed up the CPU", "Control incoming/outgoing network traffic", "Store passwords", "Defragment a disk", "B"),
    ("In a relational database, what is a primary key used for?", "To sort records alphabetically", "To uniquely identify a record", "To store images", "To encrypt tables", "B"),
    ("Which SQL command is used to retrieve data?", "INSERT", "DELETE", "SELECT", "UPDATE", "C"),
    ("What is an algorithm?", "A type of programming language", "A step-by-step method to solve a problem", "A computer virus", "A hardware component", "B"),
    ("What is the purpose of a validation check?", "To make data smaller", "To ensure data is sensible/acceptable", "To increase FPS in games", "To convert text to binary", "B"),
]

def main():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.executemany("""
        INSERT INTO Question (QuestionText, OptionA, OptionB, OptionC, OptionD, CorrectOption)
        VALUES (?, ?, ?, ?, ?, ?)
    """, QUESTIONS)

    conn.commit()
    conn.close()
    print(f"Inserted {len(QUESTIONS)} questions.")

if __name__ == "__main__":
    main()