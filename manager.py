import sqlite3

class Message:
    def __init__(self, id=0, text="", date=0.0, reply_to_id=0):
        self.id = id
        self.text = text
        self.date = date
        self.reply_to_id = reply_to_id

    def loads(self, msg):
        self.id = msg["id"]
        self.date = msg["date"]
        self.reply_to_id = msg["reply_to_message_id"]
        self.text = msg["content"]["text"]["text"]
    
    def dumps(self, message):
        msg = {
            "id": self.id,
            "date": self.date,
            "reply_to_message_id": self.reply_to_id,
            "content": {
                "text": {
                    "text": self.text
                }
            }
        }
        return msg        

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
    def __exit__(self):
        self.conn.close()