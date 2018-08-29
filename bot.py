import telebot
from take_screenshot import *

TOKEN = "652964125:AAFDvCnJGPueErD8rpyXEslwuql45zzZ6W4"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['get'])
def start_handler(message):
    bot.send_message(message.chat.id, 'Привет, скоро я буду парсить с параметрами(Test version)')
    update_with_cashe()
    f = open(get_img_name(),"rb")
    bot.send_photo(message.chat.id,f)
    f.close()

bot.polling()