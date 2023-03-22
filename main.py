import openai
import telebot
from configparser import ConfigParser

config = ConfigParser()

config.read('api_key.ini')

BOT_TOKEN = config.get('openai', 'bot_token')
OPENAI_TOKEN = config.get('openai', 'openai_token')

openai.api_key = OPENAI_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

chat_messages = [{'role': "user", "content": "Привіт"}]


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_messages.clear()
    bot.reply_to(message, "Привіт. чим можу допомогти?")


@bot.message_handler(func=lambda message: True)
def send_welcome(message):
    result = ''
    question = message.text
    chat_messages.append({'role':  "user", "content": question})
    try:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=chat_messages,)
    
        for choice in response.choices:
            result += choice.message.content
    
    except ConnectionResetError:
        result = 'помилка підключення до мережі. спробуйте ще раз'
    

    bot.reply_to(message, result)

bot.infinity_polling()
