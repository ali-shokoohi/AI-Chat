from telegram.client import Telegram
from datetime import datetime
from manager import Message
from secrets import API_ID, API_HASH, PHONE, DATABASE_ENCRYPTION_KEY
import logging

logging.basicConfig(filename='./logs/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("root")
logger.warning('This is a Warning')

tg = Telegram(
    api_id=API_ID,
    api_hash=API_HASH,
    phone=PHONE,
    database_encryption_key=DATABASE_ENCRYPTION_KEY,
)

me = 715550983  # Bot ID

message = Message()


def main():
    tg.login()
    # if this is the first run, library needs to preload all chats
    # otherwise the message will not be sent
    result = tg.get_chats()
    result.wait()

#    Check the chat_id is for groups or private chats
    def is_private(chat_id):
        if str(chat_id)[0] == '-':
            return False
#       elif ...:
#           return False
        else:
            return True
    
#    Text message handler
    def message_handler(update):
        user_id = update["message"]["sender_user_id"]
        chat_id = update["message"]["chat_id"]
        message_entry = update["message"]
        if user_id != me:
            message.load(message_entry)
            message.save()
            reply_to_message_id = message.reply_to_id
            message_text = message.text
            warning = f"A text message has been received from {chat_id} at {datetime.now()} and that is:{message_text}"
            logger.warning(warning)
            if reply_to_message_id > 0:
                answer = "Hello human as reply!"
            else:
                answer = "Hello human!"
            
            if is_private(chat_id):
                tg.send_message(
                    chat_id=chat_id,
                    text=answer,
                )
    
#    Photo message handler
    def photo_handler(update):
        user_id = update["message"]["sender_user_id"]
        chat_id = update["message"]["chat_id"]
        if user_id != me:
            photo_content = update["message"]["content"].get("photo", {})
            photo_id = photo_content.get("id", "").lower()
            warn = f"A photo message has been received from {chat_id} at {datetime.now()} and ID of that is:{photo_id}"
            logger.warning(warn)
            
            if is_private(chat_id):
                tg.send_message(
                    chat_id=chat_id,
                    text="Nice picture human!",
                )
    
#    Unknown message handler
    def unknown_handler(update):
        user_id = update["message"]["sender_user_id"]
        chat_id = update["message"]["chat_id"]
        if user_id != me:
            logger.warning(f"A unknown message has been received from {chat_id} at {datetime.now()}")
            if is_private(chat_id):
                tg.send_message(
                    chat_id=chat_id,
                    text="What is this human?!",
                )
    
#    A function for handling new messages
    def new_message_handler(update):
        message_type = update["message"]["content"]["@type"]
        # If message is a text
        if message_type == "messageText":
            message_handler(update)
        elif message_type == "messagePhoto":  # If message is a photo
            photo_handler(update)
#            elif message_type == ...:
#                ..._handler(update)
        else:  # If message is a unknown type
            unknown_handler(update)

    logger.warning(result.update)
    tg.add_message_handler(new_message_handler)
    tg.idle()  # blocking waiting for CTRL+C

# Run bot


if __name__ == "__main__":
    main()
