import telebot
import cherrypy
from telebot import types

from take_screenshot import *

TOKEN = "464958591:AAGQ6-sdh0M_L_zq9GnfmwC8NCvV7ryjbe8"

WEBHOOK_HOST = 'IP-адрес сервера, на котором запущен бот'
WEBHOOK_PORT = 443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (TOKEN)


bot = telebot.TeleBot(TOKEN)

groups_id = [6949772, 6949830, 6949706, 6949774, 7195531, 6949688, 6949724, 6949726, 6949654, 7195529, 7195533]


# Наш вебхук-сервер
class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


def send_time_table(chat_id, group_id=groups_id[4]):
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


@bot.message_handler(commands=['start', 'go'])
def get_handler(message):
    bot.send_message(message.chat.id, 'Welcome!\nНапиши /get - для парса свежего расписание ПЗПИ-18')


@bot.message_handler(commands=['get'])
def test_handler(message):
    keyboard = types.InlineKeyboardMarkup()
    row = []
    for i in range(1, 12):
        callback_button = types.InlineKeyboardButton(text=str(i), callback_data=str(i - 1))
        row.append(callback_button)
        if i == 6 or i == 11:
            keyboard.row(*row)
            row = []

    bot.send_message(message.chat.id, "Какой группы расписание Вы желаете?", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    id_group = int(call.data)
    if id_group >= 0 and id_group <= 11:
        send_time_table(call.message.chat.id, group_id=groups_id[id_group])



# Снимаем вебхук перед повторной установкой (избавляет от некоторых проблем)
bot.remove_webhook()

 # Ставим заново вебхук
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))
# Указываем настройки сервера CherryPy
cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

 # Собственно, запуск!
cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})