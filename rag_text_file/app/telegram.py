import os
import dotenv
import telebot

dotenv.load_dotenv()


class Telegram:
    def __init__(self, message_handler):
        self.bot = telebot.TeleBot(os.getenv("TELEGRAM_API_KEY"), parse_mode=None)
        self.message_handler = message_handler

    def start(self):
        @self.bot.message_handler(func=lambda message: True)
        def handle_message(message):
            self.message_handler(message.text, message.chat.id)

        self.bot.polling()

    def send_message(self, chat_id, response):
        self.bot.send_message(chat_id, response)
