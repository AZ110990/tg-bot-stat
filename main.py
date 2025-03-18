import os
import telebot
from telebot import types
from data_manager import *

from dotenv import load_dotenv
load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN_BOT_API_TEST'))

class Dialog:
    mode = ""
    data = None

dialog = Dialog()
user_data = {}
# bot = telebot.TeleBot(os.environ.get('TOKEN_BOT_API_TEST'))

#--------------list of commands for bot menu (left side menu)--------------------
commands = {
        "start": "Главное меню бота",
        "data": "Сбор статистики",
    }

# ------------------ functions ------------------
def keyboard_data():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton('Яйца 🥚', callback_data='eggs'),
        types.InlineKeyboardButton('Среднее', callback_data='average')
    )
    return keyboard

def work_with_data(call):
    keyboard = keyboard_data()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Вы выбрали работу с данными. Что хотите сделать?:',
                          reply_markup=keyboard)

def save_data(message):
    try:
        value = int(message.text)
    except ValueError:
        bot.send_message(chat_id=message.chat.id, text=f"Напишите цифру, не текст")
    else:
        notification = put_data(value)
        bot.send_message(chat_id=message.chat.id, text=notification)

# --------------------- bot ---------------------
@bot.message_handler(commands=['start'])
def start(message):
    command_list = [types.BotCommand(key, value) for key, value in commands.items()]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton('Работа с Данными', callback_data='data'),
        types.InlineKeyboardButton('Игры', callback_data='games')
    )
    bot.set_my_commands(command_list, scope=types.BotCommandScopeChat(chat_id=message.chat.id))
    #bot.set_chat_menu_button(menu_button=types.MenuButtonCommands(), chat_id=message.chat.id)
    bot.send_message(chat_id=message.chat.id, text="Привет! Что бы ты хотел сделать?", reply_markup=keyboard)


@bot.message_handler(commands=['data'])
def work_with_data_menu(message):
    keyboard = keyboard_data()
    bot.send_message(chat_id=message.chat.id, text='Вы выбрали работу с данными. Что хотите сделать?', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def handle_message(message):
    if dialog.mode == "eggs":
        save_data(message)
    elif message.text.startswith('/'):
        bot.send_message(chat_id=message.chat.id, text="Неизвестная команда.")
    else:
        bot.send_message(chat_id=message.chat.id, text='Выберите команду из Меню')


@bot.callback_query_handler(func=lambda call: True)
def button_handler(call):
    bot.answer_callback_query(callback_query_id=call.id)
    if call.data == "data":
        dialog.mode = "data"
        keyboard = keyboard_data()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы выбрали работу с данными. Что хотите сделать?:',
                              reply_markup=keyboard)
    elif call.data == "eggs":
        dialog.mode = "eggs"
        bot.send_message(chat_id=call.message.chat.id, text='Напишите число яиц:')
        bot.register_next_step_handler(call.message, save_data)
    elif call.data == "average":
        dialog.mode = "average"
        data = get_data()
        bot.send_message(chat_id=call.message.chat.id, text=data)
    elif call.data == "games":
        bot.send_message(chat_id=call.message.chat.id, text='Эта часть еще 🚧 🏗 🚧')
    else:
        bot.send_message(chat_id=call.message.chat.id, text='Такого мы еще не проходили. Воспользуйтесь меню')


# ---------------- local testing ----------------
if __name__ == '__main__':
    bot.infinity_polling()
