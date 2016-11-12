import telebot
from secret_vars import *
from game import Game

bot = telebot.TeleBot(TOKEN)
id = ''

@bot.message_handler(commands=['newgame'])
def send_welcome(message):
    bot.send_message(message.chat.id, '')
    id = bot.send_message(message.chat.id, 'test')

@bot.message_handler(commands=['endgame'])
def end_game(message):
    bot.send_message(message.chat.id, 'THATS CAPS :clap: :clap: :clap:')
    bot.edit_message_text(self, 'test2', message.chat.id, id)

bot.polling()
