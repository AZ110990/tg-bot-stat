import os
import random
import telebot
from telebot import types
from datetime import datetime
from data_manager import *

from dotenv import load_dotenv
load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN_BOT_API_TEST'))

class Dialog:
    mode = None
    data = None

dialog = Dialog()
user_data = {}
# bot = telebot.TeleBot(os.environ.get('TOKEN_BOT_API_TEST'))

#------------------------list of commands for bot menu (left side menu)------------------------------------------------
commands = {
        "start": "Главное меню бота",
        "data": "Сбор статистики-фигистики",
    }
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
    bot.set_chat_menu_button(menu_button=types.MenuButtonCommands(), chat_id=message.chat.id)
    bot.send_message(chat_id=message.chat.id, text="Привет! Что бы ты хотел сделать?", reply_markup=keyboard)
    #
    # markup = telebot.types.InlineKeyboardMarkup()
    # btn1 = telebot.types.InlineKeyboardButton('Работа с данными', callback_data='work_with_data')
    # btn2 = telebot.types.InlineKeyboardButton('Игры', callback_data='games')
    # markup.add(btn1, btn2)
    # bot.send_message(chat_id=message.chat.id, text='Выберите действие:', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_message(message):
    if dialog.mode == "eggs":
        dialog.data = int(message.text)
        bot.send_message(chat_id=message.chat.id, text=f'Вы ввели: {dialog.data}')
        dialog.mode = None
    else:
        bot.send_message(chat_id=message.chat.id, text='Выберите команду из Меню')


@bot.message_handler(commands=['data'])
def work_with_data_menu(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton('Яйца 🥚', callback_data='eggs'),
        types.InlineKeyboardButton('Среднее', callback_data='average')
    )
    # bot.send_message(chat_id=message.chat.id, text='Вы выбрали работу с данными. Что хотите сделать?',
    #                  reply_markup=keyboard)
    bot.send_message(chat_id=message.chat.id, text="Привет! Что бы ты хотел сделать?", reply_markup=keyboard)
#
# @bot.callback_query_handler(func=lambda call: call.data == 'data')
# def work_with_data(call):
#     keyboard = types.InlineKeyboardMarkup()
#     keyboard.row(
#         types.InlineKeyboardButton('Яйца 🥚', callback_data='eggs'),
#         types.InlineKeyboardButton('Среднее', callback_data='average')
#     )
#     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                           text='Вы выбрали работу с данными. Что хотите сделать?:',
#                           reply_markup=keyboard)
#
#
# @bot.message_handler(content_types=['text'])
# def unknown(message):
#     if message.text.startswith('/'):
#         bot.send_message(chat_id=message.chat.id, text="Неизвестная команда.")
#
# # @bot.callback_query_handler(func=lambda call: True)
# # def button_handler(call):
# #     bot.answer_callback_query(callback_query_id=call.id)
# #     if call.data == "data":
# #         work_with_data(call.message)
# #     elif call.data == "eggs":
# #         dialog.mode = "eggs"
# #         bot.send_message(chat_id=call.message.chat.id, text='Напишите число яиц:')
# #     elif call.data == "average":
# #         get_data(call.message)
# #     elif call.data == "games":
# #         bot.send_message(chat_id=call.message.chat.id, text='Эта часть еще 🚧 🏗 🚧')
# #     else:
# #         bot.send_message(chat_id=call.message.chat.id, text='Такого мы еще не проходили. Воспользуйтесь меню')
#
# @bot.callback_query_handler(func=lambda call: call.data == 'eggs')
# def work_with_data(call):
#     bot.send_message(chat_id=call.message.chat.id, text='Напишите число:')
#     bot.register_next_step_handler(call.message, save_data)
#
# # Функция для сохранения данных пользователя
# def save_data(message):
#     user_id = message.chat.id
#     user_data[user_id] = int(message.text)
#     bot.send_message(chat_id=message.chat.id, text=f'Данные сохранены: {user_data[user_id]}')
#
# @bot.callback_query_handler(func=lambda call: call.data == 'average')
# def get_data(call):
#     pass

# ---------------- local testing ----------------
if __name__ == '__main__':
    bot.infinity_polling()
