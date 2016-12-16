import telebot
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
    names = [x[1:] for x in message.text.split() if '@' in x]

    if(len(names) != 4):
        bot.send_message(message.chat.id, 'Error, need exactly four players')
        return

    new_game = Game(names, message.from_user.username, message.message_id)

    markup = create_markup(new_game)

    sent_message = bot.send_message(
            message.chat.id, 
            'Game ID: '+sent_message.message_id+'\n'+
            get_score_text(new_game), reply_markup=markup)

    games.update({sent_message.message_id:new_game})

@bot.message_handler(commands=['deuces'])
def deuces(message):
    try:
        game = games[message.text]
        game.set_deuces()
    except KeyError:
        bot.send_message(
                message.chat.id,
                'Wrong ID or something idk. How did you fuck this up?')

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(callback):
    try:
        #get the game the current message is referencing
        game_id = callback.message.message_id
        game = games[game_id]
    except KeyError:
        print('oh well')
        return

    #validate the person pressing a button is allowed to
    if not callback.from_user.username == game.get_owner():
        print(callback.from_user.username)
        return

    #check if end button was pressed
    if callback.data =='end':
        end_game(game)
        return
    else:
        update_score(game, callback.data)

#helper functions :)
def update_score(game, scorer):
    #update the score
    game.update_score(scorer)

    #get the markup
    markup = create_markup(game)

    bot.edit_message_text(
            chat_id=callback.message.chat.id,message_id=game_id,
            text='Game ID: '+sent_message.message_id+'\n'+
            get_score_text(game),reply_markup=markup)

def end_game(game):
    try:
        score = game.get_score()
        teams = games.get_teams()
        bot.send_message(game.get_id(), 'Final Score: %s: %d  %s: %d\n'%
                (teams[0],score[0],teams[1],score[1]) + 'THAT\'S CAPS ')

        del games[game.get_id()]
    except KeyError:
        return

def create_markup(game):
    names = game.get_names()
    scores = game.get_individual_scores()

    markup = types.InlineKeyboardMarkup()

    itembtn0 = types.InlineKeyboardButton(
            "%s: %d"%(names[0], scores[0]), callback_data=names[0])
    itembtn1 = types.InlineKeyboardButton(
            "%s: %d"%(names[1], scores[1]), callback_data=names[1])
    markup.row(itembtn0,itembtn1)

    itembtn2 = types.InlineKeyboardButton(
            "%s: %d"%(names[2], scores[2]), callback_data=names[2])
    itembtn3 = types.InlineKeyboardButton(
            "%s: %d"%(names[3], scores[3]), callback_data=names[3])
    markup.row(itembtn2,itembtn3)

    itemend = types.InlineKeyboardButton('End Game', callback_data='end')
    if game.deuces():
        itemdeuces = types.InlineKeyboardButton('Deuces!!!!', callback_data='end')
        markup.row(itemdeuces,itemend)
    else:
        markup.row(itemend)

    return markup

def get_score_text(game):
    #get the team names and score
    team1, team2 = game.get_teams()
    score1, score2 = game.get_score()

    #update the message 
    update_text = '%s: %d\n%s: %d' % (team1, score1, team2, score2)

    return update_text

bot.polling()
