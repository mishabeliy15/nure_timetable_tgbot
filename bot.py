import telebot
from telebot import types

from take_screenshot import *

TOKEN = ""
bot = telebot.TeleBot(TOKEN)

groups_id =[6949772, 6949830, 6949706, 6949774, 7195531, 6949688, 6949724, 6949726, 6949654, 7195529, 7195533]


def send_time_table(chat_id,group_id=groups_id[4]):
    update_with_cashe(group_id)
    try:
        f = open(get_img_name(group_id), "rb")
        bot.send_photo(chat_id, f)
        f.close()
    except FileNotFoundError:
        bot.send_message(chat_id, "FileNotFound\nВозможно сайт ХНУРЭ недоступен.")
        logging("Error: FileNotFound (send_time_table)")

@bot.message_handler(commands=['author'])
def get_handler(message):
    bot.send_message(message.chat.id, 'Author: Misha Beliy(@devexc)')

@bot.message_handler(commands=['start','go'])
def get_handler(message):
    bot.send_message(message.chat.id, 'Welcome!\nНапиши /get - для парса свежего расписание ПЗПИ-18')

@bot.message_handler(commands=['get'])
def test_handler(message):
    keyboard = types.InlineKeyboardMarkup()
    row =[]
    for i in range(1,12):
        callback_button = types.InlineKeyboardButton(text=str(i), callback_data=str(i-1))
        row.append(callback_button)
        if i==6 or i==11:
            keyboard.row(*row)
            row=[]

    bot.send_message(message.chat.id, "Какой группы расписание Вы желаете?",reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    id_group = int(call.data)
    if id_group>=0 and id_group<=11:
        send_time_table(call.message.chat.id,group_id=groups_id[id_group])

bot.polling(none_stop=True)
