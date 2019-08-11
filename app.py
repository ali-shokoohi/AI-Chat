from pyrogram import Client, MessageHandler
from datetime import datetime
from manager import Message, admin_workspace
from secrets import API_ID, API_HASH, PHONE, DATABASE_ENCRYPTION_KEY
import logging

logging.basicConfig(filename='./logs/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("root")
logger.warning('This is a Warning')

app = Client(
    session_name="my_account",
    api_id=API_ID,
    api_hash=API_HASH,
    phone_number=PHONE
)

me = 715550983  # Bot ID

admins = {"ali": 554868848}

message = Message()


def main():
    # if this is the first run, library needs to preload all chats
    # otherwise the message will not be sent
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
        message.load(update)
        user_id = update.from_user.id
        # When admin send a command as a private message
        if (user_id == message.chat_id) and (user_id in admins.values()):
            response = admin_workspace(message)
            status = response["status"]
            if status == "ok":
                info = response["info"]
                text = f"Well done:\n{info}"
                if "file" in response:
                    file = response["file"]
                    app.send_document(
                        chat_id=message.chat_id,
                        document=file,
                        caption=text,
                        reply_to_message_id=message.id
                    )
            else:
                error = response["error"]
                text = f"A error has been detected:\n{error}"
                app.send_message(
                    chat_id=user_id,
                    text=text
                )
            return None

        if user_id != me:
            message.save()
            reply_to_message_id = message.reply_to_id
            if reply_to_message_id > 0:
                answer = "Hello human as reply!"
            else:
                answer = "Hello human!"

            if is_private(message.chat_id):
                app.send_message(
                    chat_id=message.chat_id,
                    text=answer,
                    reply_to_message_id=message.id
                )

    #    Photo message handler
    def photo_handler(update):
        user_id = update.from_user.id
        chat_id = update.chat.id
        if user_id != me:
            if is_private(chat_id):
                app.send_message(
                    chat_id=chat_id,
                    text="Nice picture human!",
                )

    #    Unknown message handler
    def unknown_handler(update):
        user_id = update.from_user.id
        chat_id = update.chat.id
        if user_id != me:
            logger.warning(f"A unknown message has been received from {chat_id} at {datetime.now()}")
            if is_private(chat_id):
                app.send_message(
                    chat_id=chat_id,
                    text="What is this human?!",
                )

    #    A function for handling new messages
    def new_message_handler(client, update):
        # Check type of message
        if update.text:  # If message is a text
            return message_handler(update)
        elif update.media:  # If message type is media
            if update.photo:
                return photo_handler(update)
        #               elif message_type == ...:
        #                   return ..._handler(update)
        else:  # If message has a unknown type
            logger.warning(update)
            return unknown_handler(update)

    handler = MessageHandler(new_message_handler)
    app.add_handler(handler)


# Run bot


if __name__ == "__main__":
    main()
    app.run()  # blocking waiting for CTRL+C
