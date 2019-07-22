from telegram.client import Telegram
from datetime import datetime
import time

tg = Telegram(
    api_id='649592',
    api_hash='5f8054cf94fa09a99de547f7013600ab',
    phone='+989211373922',
    database_encryption_key='changekey123',
)

me = 715550983

def main():
    tg.login()
    # if this is the first run, library needs to preload all chats
    # otherwise the message will not be sent
    result = tg.get_chats()
    result.wait()

    def is_private(chat_id):
        if str(chat_id)[0] == '-':
            return False
#       elif ...:
#           return False
        else:
            return True        

    def new_message_handler(update):
        user_id = update['message']['sender_user_id']
        chat_id = update['message']['chat_id']
        if (user_id != me) and is_private(chat_id):
            message_content = update['message']['content'].get('text', {})
            # we need this because of different message types: photos, files, etc.
            message_text = message_content.get('text', '').lower()
            print(f'A message has been received from {chat_id} at {datetime.now()} and that is:\n{message_text}')
            tg.send_message(
                chat_id=chat_id,
                text='Hello human!',
            )
    print(result.update)
    tg.add_message_handler(new_message_handler)
    tg.idle()  # blocking waiting for CTRL+C

if __name__ == "__main__":
    main()
