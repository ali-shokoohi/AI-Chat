import sqlite3

class Data:
    def __init__(self, location="./database/data.db"):
        #Connect to database
        self.conn = sqlite3.connect(location, check_same_thread=False)
        self.c = self.conn.cursor()

        #Create messages table if not exists
        self.c.execute('''CREATE TABLE IF NOT EXISTS messages
             (pk INTEGER PRIMARY KEY AUTOINCREMENT, id INTEGER, text TEXT, date REAL, reply_to_id INTEGER)''')
    def insert(self, id, text, date, reply_to_id):
        self.c.execute(f"""INSERT INTO messages (
            id, text, date, reply_to_id
        ) VALUES (
            '{id}', '{text}', '{date}', '{reply_to_id}'
            )"""
        )
        self.conn.commit()
    def __exit__():
        self.conn.close()