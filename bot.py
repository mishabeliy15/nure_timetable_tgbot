import telebot
from take_screenshot import update_photo

TOKEN = ""
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['get'])
def start_handler(message):
    bot.send_message(message.chat.id, 'Привет, скоро я буду парсить с параметрами(Test version)')
    update_photo()
    f = open("img.jpg","rb")
    bot.send_photo(message.chat.id,f)
    f.close()

bot.polling()