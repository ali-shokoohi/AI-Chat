from telegram.client import Telegram
from datetime import datetime
import time

tg = Telegram(
    api_id='649592',
    api_hash='5f8054cf94fa09a99de547f7013600ab',
    phone='+989211373922',
    database_encryption_key='changekey123',
)

me = 715550983 #Bot ID

def main():
    tg.login()
    # if this is the first run, library needs to preload all chats
    # otherwise the message will not be sent
    result = tg.get_chats()
    result.wait()

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
        user_id = update['message']['sender_user_id']
        chat_id = update['message']['chat_id']
        if (user_id != me) and is_private(chat_id):
            message_content = update['message']['content'].get('text', {})
            message_text = message_content.get('text', '').lower()
            print(f'A text message has been received from {chat_id} at {datetime.now()} and that is:\n{message_text}')
            tg.send_message(
                chat_id=chat_id,
                text='Hello human!',
            )
    
    #Photo message handler
    def photo_handler(update):
        user_id = update['message']['sender_user_id']
        chat_id = update['message']['chat_id']
        if (user_id != me) and is_private(chat_id):
            photo_content = update['message']['content'].get('photo', {})
            photo_id = photo_content.get('id', '').lower()
            print(f'A photo message has been received from {chat_id} at {datetime.now()} and ID that is:\n{photo_id}')
            tg.send_message(
                chat_id=chat_id,
                text='Nice picture human!',
            )
    
    #Unknown message handler
    def unknown_handler(update):
        user_id = update['message']['sender_user_id']
        chat_id = update['message']['chat_id']
        if (user_id != me) and is_private(chat_id):
            print(f'A unknown message has been received from {chat_id} at {datetime.now()}')
            tg.send_message(
                chat_id=chat_id,
                text='What is this human?!',
            )
    
    #A function for handlling new messages
    def new_message_handler(update):
        message_type = update["message"]["content"]["@type"]
        if message_type == "messageText":#If message is a text
            message_handler(update)
        elif message_type == "messagePhoto":#If message is a photo
            photo_handler(update)
#        elif message_type == ...:
#            ..._handler(update)
        else:#If messgae is a unknown type
            unknown_handler(update)

    print(result.update)
    tg.add_message_handler(new_message_handler)
    tg.idle()  # blocking waiting for CTRL+C

#Run bot
if __name__ == "__main__":
    main()
