import os
import time

import dotenv
import telebot

dotenv.load_dotenv()


class Telegram:
    def __init__(self, message_handler):
        self.bot = telebot.TeleBot(os.getenv("TELEGRAM_API_KEY"), parse_mode=None)
        self.message_handler = message_handler

    def start(self):
        def run_polling():
            while True:
                try:
                    self.bot.polling(non_stop=True)  # non_stop=True makes the bot continuously poll
                except Exception as e:
                    print(f"Polling error: {e}")
                    time.sleep(5)

        @self.bot.message_handler(func=lambda message: True)
        def handle_message(message):
            self.message_handler(message.text, message.chat.id)

        run_polling()

    def send_message(self, chat_id, response):
        self.bot.send_message(chat_id, response)
