import sqlite3
import json

STORE_LOCATION = 'tmp/'


class Message:
    def __init__(self, id=0, chat_id=0, text="", date=0.0, reply_to_id=0):
        # Create new Message object
        self.id = id
        self.chat_id = chat_id
        self.text = text
        self.date = date
        self.reply_to_id = reply_to_id

    def __str__(self):
        return f"<Message Object {self.id}>"

    def load(self, msg, many=False):
        if many:
            # Return multi message objects from a list
            result = list()
            for msg_o in msg:
                message = Message()
                message.load(msg_o)
                result.append(message)
            return result
        else:
            # Load Message object from a dictionary
            try:
                self.id = msg.message_id
                self.chat_id = msg.chat.id
                self.date = msg.date
                if msg.reply_to_message:
                    self.reply_to_id = msg.reply_to_message.message_id
                self.text = msg.text
                return self
            except KeyError:
                pass

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
                "chat_id": self.chat_id,
                "date": self.date,
                "reply_to_message_id": self.reply_to_id,
                "text": self.text
            }
            return msg

    @staticmethod
    def get(id=0, all=False):
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
             (pk INTEGER PRIMARY KEY AUTOINCREMENT, id INTEGER, chat_id INTEGER, text TEXT, date TEXT, reply_to_id INTEGER)''')

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
                id, chat_id, text, date, reply_to_id
            ) VALUES (
                '{message.id}', {message.chat_id}, '{message.text}', '{message.date}', '{message.reply_to_id}'
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
            message = Message(id=fetch[1], chat_id=fetch[2], text=fetch[3], date=fetch[4], reply_to_id=fetch[5])
            result.append(message)
        self.conn.close()
        return result


#    This method really useless
#    def __exit__(self):
#        self.conn.close()


# Execute admin's commands
def admin_workspace(message):
    response = dict()
    command = message.text
    try:
        if command == "/get_all":
            all_messages = Message.get(all=True)
            all_messages_dump = message.dump(messages=all_messages, many=True)
            with open(STORE_LOCATION + 'all_messages.json', 'w', encoding='utf-8') as f:
                json.dump(obj=all_messages_dump, fp=f, indent=4)
                f.close()
            response["status"] = "ok"
            response["info"] = f"All messages saved in: {STORE_LOCATION}all_messages.json"
        # elif command == "...":
            # response = ...
        else:
            response["status"] = "bad"
            response["error"] = "Your command is undefined!"
    except Exception as error:
        response["status"] = "bad"
        response["error"] = error
    return response
