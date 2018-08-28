import telebot
from take_screenshot import update_photo

TOKEN = ""
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['get'])
def start_handler(message):
    bot.send_message(message.chat.id, 'Привет, когда я вырасту, я буду парсить с параметрами')
    update_photo()
    img = open("out.jpg","rb")
    bot.send_photo(message.chat.id,img)
    img.close()

bot.polling()