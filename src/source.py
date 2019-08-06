import peewee
import os
from telebot.types import InlineQueryResultArticle
from telebot.types import InputTextMessageContent

from flask import Flask, request

db=peewee.SqliteDatabase('users.db')

class User(peewee.Model):
    chat_id = peewee.IntegerField(unique=True)
    state = peewee.IntegerField(default=0)
    class Meta:
        database=db

def init():
    db.connect()
    db.create_tables([User],safe=True)
    db.close()
def get_state(chat_id):
    user=User.get_or_none(chat_id=chat_id)
    if user is None:
        return -1
    return user.state
def set_state(chat_id,state):
    user,created=User.get_or_create(chat_id=chat_id)
    user.state=state
    user.save()
init()




import telebot

API_TOKEN=os.getenv('TG_API_TOKEN')
bot=telebot.TeleBot(API_TOKEN,skip_pending=True)
server=Flask(__name__)
q=['Ты человек или automata de merde?','Тебе нужны красивые желтые перчатки для работы?','?','Как выглядят те самые люди, которые ботов пишут?','Ты победил. Начнем снова.']
a=['человек','да','!','как люди, которые ботов пишут']


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id,text="ghbdtn")
    set_state(message.chat.id,0)
    quest(message.chat.id)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    fforward_from=None
    if message.forward_from is None:
        fforward_from=message.from_user
    else:
        fforward_from=message.forward_from
    bot.send_message(chat_id=message.chat.id,text="Имя: "+fforward_from.first_name+"\nФамилия: "+fforward_from.last_name+"\nID: "+str(fforward_from.id)+"\nUsername: "+fforward_from.username+"\nChat ID: "+str(message.chat.id))

@bot.inline_handler(func=lambda query:"алиас" in query.query)
def answer_alias_query(inline_query):
    username=inline_query.from_user.username
    alias_artice=InlineQueryResultArticle(
        id='0',
        title='Кто я такой?',
        description='Я такой кто?',
        input_message_content=InputTextMessageContent(
            message_text="Имя: "+fforward_from.first_name+"\nФамилия: "+fforward_from.last_name+"\nID: "+str(fforward_from.id)+"\nUsername: "+fforward_from.username+"\nChat ID: "+str(message.chat.id)
        )
    )
    bot.answer_inline_query(
        inline_query_id=inline_query.id,
        results=[alias_artice],
        cache_time=0
    )
@server.route('/'+API_TOKEN,methods=['POST'])
def get_message():
    json_update=request.stream.read().decode('utf-8')
    update=telebot.types.Update.de_json(json_update)

    bot.process_new_updates([update])

    return '', 200


if __name__=='__main__':
    bot.remove_webhook()
    bot.set_webhook(url=os.getenv('WEBHOOK_URL')+API_TOKEN)
    server.run(host="0.0.0.0",
               port=int(os.getenv('PORT',8443)))

