import telebot
import re
import random
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
    forbidden_names = ['caps_control_bot', 'end', 'deuces']
    names = [x[1:] for x in message.text.split() if '@' in x and not any(y in x for y in forbidden_names)]

    if(len(names) != 4):
        bot.send_message(message.chat.id, 'Error, need exactly four players')
        return

    new_game = Game(names, message.from_user.username, message.chat.id)

    markup = create_markup(new_game)

    sent_message = bot.send_message(
            message.chat.id, 
            text='Game ID: '+str(message.message_id + 1)+'\n'+
            get_score_text(new_game), reply_markup=markup)

    new_game.set_game_id(sent_message.message_id)

    games.update({sent_message.message_id:new_game})

@bot.message_handler(commands=['deuces'])
def deuces(message):
    game_id = message.text.split()[1]

    try:
        game = games[int(game_id)]
        if game.set_deuces():
            update_message(game)
            deuced(game)

    except KeyError:
        bot.send_message(
                message.chat.id,
                'Wrong ID or something idk. How did you fuck this up?')

@bot.message_handler(commands=['neweuph'])
def neweuph(message):
    if(message.text == '/neweuph' or message.text == '/neweuph@caps_control_bot'):
        return

    verbf = open('verb', 'a')
    nounf = open('noun', 'a')

    split = re.findall('\([\w|\ ]+\)',message.text)
    verb = split[0][1:len(split[0])-1]
    noun = split[1][1:len(split[1])-1]

    verbf.write(verb + '\n')
    nounf.write(noun + '\n')

    verbf.close()
    nounf.close()

@bot.message_handler(commands=['ask2play'])
def ask2play(message):
    asks = open('ask','r').read().splitlines()
    nouns = open('noun','r').read().splitlines()
    verbs = open('verb','r').read().splitlines()

    ask = random.choice(asks)
    noun = random.choice(nouns)
    verb = random.choice(verbs)

    bot.send_message(message.chat.id, 
            ask + ' ' + verb +' the ' + noun + '?')

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(callback):
    try:
        #get the game the current message is referencing
        game = games[callback.message.message_id]
    except KeyError:
        print('Game Does Not Exist: ' + string(callback.message.message_id))
        return

    #validate the person pressing a button is allowed to
    if not callback.from_user.username == game.get_owner():
        print('Illegal user: ' + callback.from_user.username + ': ' + callback.data)
        return

    #check if end button was pressed
    if callback.data =='end':
        end_game(game)
        return
    elif callback.data=='deuces_button':
        deuced(game)
    else:
        update_score(game, callback.data)

#helper functions :)
def deuced(game):
    if game.deuced():
        update_message(game)

def update_message(game):
    #get the markup
    markup = create_markup(game)

    bot.edit_message_text(
            chat_id=game.get_chat_id(),message_id=game.get_game_id(),
            text='Game ID: '+str(game.get_game_id())+'\n'+
            get_score_text(game),reply_markup=markup)

def update_score(game, scorer):
    #update the score
    game.update_score(scorer)

    #update the message
    update_message(game)


def end_game(game):
    try:
        score = game.get_score()
        teams = game.get_teams()
        bot.send_message(game.get_chat_id(), 'Final Score: %s: %d  %s: %d\n'%
                (teams[0],score[0],teams[1],score[1]) + u'THAT\'S CAPS \U0001f44f \U0001f44f \U0001f44f')

        del games[game.get_game_id()]
    except KeyError:
        return

def create_markup(game):
    names = game.get_names()
    scores = game.get_individual_scores()

    markup = types.InlineKeyboardMarkup()

    itembtn0 = types.InlineKeyboardButton(
            '%s: %d'%(names[0], scores[0]), callback_data=names[0])
    itembtn1 = types.InlineKeyboardButton(
            '%s: %d'%(names[1], scores[1]), callback_data=names[1])
    markup.row(itembtn0,itembtn1)

    itembtn2 = types.InlineKeyboardButton(
            '%s: %d'%(names[2], scores[2]), callback_data=names[2])
    itembtn3 = types.InlineKeyboardButton(
            '%s: %d'%(names[3], scores[3]), callback_data=names[3])
    markup.row(itembtn2,itembtn3)

    itemend = types.InlineKeyboardButton('End Game', callback_data='end')
    if game.get_deuces():
        itemdeuces = types.InlineKeyboardButton('Deuces!!!!', callback_data='deuces_button')
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

while True:
    bot.polling()
