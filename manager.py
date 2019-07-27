import sqlite3


class Message:
    def __init__(self, id=0, text="", date=0.0, reply_to_id=0):
        # Create new Message object
        self.id = id
        self.text = text
        self.date = date
        self.reply_to_id = reply_to_id
    
    def __str__(self):
        return f"<Message Object {self.id}>"

    def load(self, msg, many=False):
        if many:
            # Return multi message objects from a list
            result = list()
            m_dict = dict()
            for msg_o in msg:
                m_dict["id"] = msg_o["id"]
                m_dict["date"] = msg_o["date"]
                m_dict["reply_to_id"] = msg_o["reply_to_message_id"]
                m_dict["text"] = msg_o["content"]["text"]["text"]
#                Use This method again for load m_dict to a Message object
                message = Message()
                message.load(m_dict)
                result.append(message)
            return result
        else:
            # Load Message object from a dictionary
            self.id = msg["id"]
            self.date = msg["date"]
            self.reply_to_id = msg["reply_to_message_id"]
            self.text = msg["content"]["text"]["text"]
            return self
    
    def dump(self, messages=None, many=False):
        if many:
            # Return a list of dictionaries from multi message objects
            result = list()
            for message in messages:
                result.append(message.dump())
            return result
        else:
            # Convert Message object to a dictionary
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

    def get(self, id=0, all=False):
        data = Data()
        if all:
            # Return all messages
            result = data.get(all=True)
        else:
            # Return the message that message_id === id
            result = data.get(id=id)
        return result

    def save(self, message=None, many=False):
        data = Data()
        if many:
            # Save multi message objects to database directly
            result = data.insert(message=message, many=True)
        else:
            # Save message object to database directly
            result = data.insert(message=self)
        return result


class Data:
    def __init__(self, location="./database/data.db"):
        # Connect to database
        self.conn = sqlite3.connect(location, check_same_thread=False)
        self.c = self.conn.cursor()

        # Create messages table if not exists
        self.c.execute('''CREATE TABLE IF NOT EXISTS messages
             (pk INTEGER PRIMARY KEY AUTOINCREMENT, id INTEGER, text TEXT, date REAL, reply_to_id INTEGER)''')

    def insert(self, message, many=False):
        if many:
            # Insert multi message objects to messages table
            result = list()
            for msg in message:
                save = msg.save()
                result.append(save)
            return result
        else:
            # Insert new message object to messages table
            self.c.execute(f"""INSERT INTO messages (
                id, text, date, reply_to_id
            ) VALUES (
                '{message.id}', '{message.text}', '{message.date}', '{message.reply_to_id}'
                )"""
            )
            # Commit insert
            self.conn.commit()
            self.conn.close()
            return message

    def get(self, id=0, all=False):
        if all:
            # Return all messages
            self.c.execute('SELECT * FROM messages')
        else:
            # Return the message that message_id === id
            message_id = (id,)
            self.c.execute('SELECT * FROM messages WHERE id=?', message_id)
        fetchall = self.c.fetchall()
        result = list()
        for fetch in fetchall:
            message = Message(id=fetch[1], text=fetch[2], date=fetch[3], reply_to_id=fetch[4])
            result.append(message)
        self.conn.close()
        return result
#    This method really useless
#    def __exit__(self):
#        self.conn.close()
