import sqlite3

database = sqlite3.connect("db.db")
cursor = database.cursor()

try:
    # creates table with new users and their referrals
    cursor.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        user_id TEXT,
        user_username TEXT,
        history TEXT,
        message_id TEXT,
        busy BOOLEAN DEFAULT FALSE,
        counter INTEGER DEFAULT 0
        )''')

except:
    print('Users table already exists.')


# cursor.execute("DELETE FROM referrals WHERE id<>1000")
# database.commit()