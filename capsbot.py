import telebot
import emoji
from telebot import types
from secret_vars import *
from game import Game

bot = telebot.TeleBot(TOKEN)

games = {} #the games dictionary

#someone wants to start a new game
#create a new game object
#parse the team names from the message
#create the markup
#create the game
#send the message
#finally, add the game to the games dict using the message id to keep track
@bot.message_handler(commands=['newgame'])
def send_welcome(message):
    try:
        command,team1,team2 = message.text.split() 
    except ValueError:
        team1 = 'team1'
        team2 = 'team2'

    markup = create_markup(team1,team2)

    new_game = Game(team1,team2)

    sent_message = bot.send_message(message.chat.id, 'How to use: Press the team\'s button when they score!!\n'+
            team1 +': 0\n' + team2 +': 0', reply_markup=markup)
    id = sent_message.message_id

    games.update({id:new_game})

@bot.message_handler(commands=['endgame'])
def end_game(message):
    try:
        del games[message.message_id]
    except KeyError:
        return
    bot.send_message(message.chat.id, 'THAT\'S CAPS ')

@bot.callback_query_handler(func=lambda call: True)
def update_score(callback):
    if callback.data =='end':
        end_game(callback.message)
        return

    #the end button was not pressed
    try:
        id = callback.message.message_id
        game = games[id]

        if callback.data == '1':
            game.update_score(1,0)
        else:
            game.update_score(0,1)

        team1, team2 = game.get_names()
        score1, score2 = game.get_score()
        update_text = '%s: %d\n%s: %d' % (team1, score1, team2, score2)
        markup = create_markup(team1, team2)
        bot.edit_message_text(chat_id=callback.message.chat.id,message_id=id,text=update_text,reply_markup=markup)
    except KeyError:
        print('oh well')

#helper functions :)
def create_markup(name1, name2):
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(name1, callback_data='1')
    itembtn2 = types.InlineKeyboardButton(name2, callback_data='2')
    itemend = types.InlineKeyboardButton('End Game', callback_data='end')
    markup.row(itembtn1,itembtn2)
    markup.row(itemend)

    return markup

bot.polling()
