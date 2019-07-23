from telegram.client import Telegram
from datetime import datetime
import logging

logging.basicConfig(filename='./logs/app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("root")
logger.warning('This is a Warning')

tg = Telegram(
    api_id="649592",
    api_hash="5f8054cf94fa09a99de547f7013600ab",
    phone="+989211373922",
    database_encryption_key="changekey123",
)

me = 715550983 #Bot ID

data = {}

def main():
    tg.login()
    # if this is the first run, library needs to preload all chats
    # otherwise the message will not be sent
    result = tg.get_chats()
    result.wait()

    #New data
    def new_data(message):
        """
        data = {
            message_id:{
                date: 2019-07-17 5123546,
                message_text: SOME_TEXT,
                replies: []
            }
        }
        """
        try:
            message_id = message["id"]
            message_date = message["date"]
            message_text = message["content"]["text"]["text"]
            data[message_id] = dict()
            data[message_id]["date"] = message_date
            data[message_id]["text"] = message_text
            data[message_id]["replies"] = list()

            return True
        except Exception as e:
            logger.error("A exeption has been found:", exc_info=True)
            return False

    #Insert new data message
    def insert_data(to_message, message):
        """
        data = {
            to_message_id:{
                date: 2019-07-17 5123546,
                message_text: ToMessageText,
                replies: [
                    {
                        id: message_id,
                        text: message_text
                    }
                ]
            }
        }
        """
        try:
            to_message_id = to_message["id"]
            message_id = message["id"]
            message_text = message["content"]["text"]["text"]

            if to_message_id not in data:
                new_data(to_message)

            reply = dict()
            reply["id"] = message_id
            reply["text"] = message_text
            data[to_message_id]["replies"].append(reply)
            
            return True
        except Exception as e:
            logger.error("A exeption has been found:", exc_info=True)
            return False
        

    #Check the chat_id is for groups or private chats
    def is_private(chat_id):
        if str(chat_id)[0] == '-':
            return False
#       elif ...:
#           return False
        else:
            return True
    
    #Text message handler
    def message_handler(update):
        user_id = update["message"]["sender_user_id"]
        chat_id = update["message"]["chat_id"]
        message = update["message"]
        if (user_id != me) and new_data(message):
            reply_to_message_id = message["reply_to_message_id"]
            message_content = message["content"].get("text", {})
            message_text = message_content.get("text", "").lower()
            logger.warning(f"A text message has been received from {chat_id} at {datetime.now()} and that is:\n{message_text}")
            if reply_to_message_id > 0:
                answer = "Hello human as reply!"
                to_message = tg.get_message(chat_id=chat_id, message_id=reply_to_message_id)
                to_message.wait()
                to_message = to_message.update
                insert_data(to_message=to_message, message=message)
            else:
                answer = "Hello human!"
            
            if is_private(chat_id):
                tg.send_message(
                    chat_id=chat_id,
                    text=answer,
                )
    
    #Photo message handler
    def photo_handler(update):
        user_id = update["message"]["sender_user_id"]
        chat_id = update["message"]["chat_id"]
        if (user_id != me):
            photo_content = update["message"]["content"].get("photo", {})
            photo_id = photo_content.get("id", "").lower()
            logger.warning(f"A photo message has been received from {chat_id} at {datetime.now()} and ID of that is:\n{photo_id}")
            
            if is_private(chat_id):
                tg.send_message(
                    chat_id=chat_id,
                    text="Nice picture human!",
                )
    
    #Unknown message handler
    def unknown_handler(update):
        user_id = update["message"]["sender_user_id"]
        chat_id = update["message"]["chat_id"]
        if (user_id != me):
            logger.warning(f"A unknown message has been received from {chat_id} at {datetime.now()}")
            if is_private(chat_id):
                tg.send_message(
                    chat_id=chat_id,
                    text="What is this human?!",
                )
    
    #A function for handlling new messages
    def new_message_handler(update):
        logger.warning(str(data))
        message_type = update["message"]["content"]["@type"]
        if message_type == "messageText":#If message is a text
            message_handler(update)
        elif message_type == "messagePhoto":#If message is a photo
            photo_handler(update)
    #        elif message_type == ...:
    #            ..._handler(update)
        else:#If messgae is a unknown type
            unknown_handler(update)

    logger.warning(result.update)
    tg.add_message_handler(new_message_handler)
    tg.idle()  # blocking waiting for CTRL+C

#Run bot
if __name__ == "__main__":
    main()
