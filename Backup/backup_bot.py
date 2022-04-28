# -*- coding: utf-8 -*-
# region ───╼[Imports]╾───
from typing import Union

import jsonpickle
from typing import Union

import telebot
from telebot import custom_filters
from telebot.types import BotCommandScopeChat, BotCommandScopeDefault, CallbackQuery, Message
from telebot import util
from telebot.handler_backends import State, StatesGroup  # States
from telebot.storage import StateMemoryStorage

from Config import *
from Keyboard import InlineKeyboard
# endregion ╰─╼[Imports]╾─╯

# region ───╼[Global flags]╾───
SHOW_CALLBACK_DATA = True
DEBUG_MODE = False
# endregion ╰───╼[Global flags]╾───╯

# region ───╼[Objects initialization]╾───
jsonpickle.set_encoder_options('json', ensure_ascii=False)

state_storage = StateMemoryStorage()  # ToDo: Прикрутить pickle storage
bot = telebot.TeleBot(Token, parse_mode="HTML", skip_pending=True, state_storage=state_storage)
# endregion ╰───╼[Objects initialization]╾───╯

# region ───╼[States group]╾───
class BotDataStates(StatesGroup):
	set = State()
	get = State()
	pass
# endregion ╰───╼[States group]╾───╯

# region ───╼[Handle bot commands]╾───
# region <General commands>
# region /start
@bot.message_handler(chat_id=[*AllowedUsersIDs, *AllowedGroupsID], commands=['start'], chat_types=['private','supergroup'])
@bot.callback_query_handler(func=lambda call: call.data == '/start' and call.message.chat.type in ['private', 'supergroup'])
def command_start_supergroup(call: Union[CallbackQuery, Message]):
	chat_id = call.message.chat.id if type(call) is CallbackQuery else call.chat.id
	user_id = call.message.from_user.id if type(call) is CallbackQuery else call.from_user.id
	user_name = call.message.from_user.first_name if type(call) is CallbackQuery else call.from_user.first_name
	chat_type = call.message.chat.type if type(call) is CallbackQuery else call.chat.type

	def GenerateMainMenuText(_chat_type):
		headerEmptySpaceAmount = 6
		text = '<code>{0}</code>\n' \
			   '<code>{1}</code><b>{2}</b><code>{1}</code>\n' \
			   '<code>{0}</code>\n'.format('—' * (16 + headerEmptySpaceAmount * 2), '⠀' * headerEmptySpaceAmount, 'ГОЛОВНЕ МЕНЮ')
		if _chat_type == 'supergroup':
			text = f"{text}\n" \
				   f"\n" \
				   f"<i>Користувач: <code>{user_name}</code></i>"
			return text
		else:
			return text

	# region <If inline button>
	if type(call) is CallbackQuery:
		# Якщо викликано через кнопку
		bot.answer_callback_query(call.id, f'Назад в головне меню')
		bot.edit_message_text(
			text=GenerateMainMenuText(chat_type),
			chat_id=chat_id,
			message_id=call.message.message_id,
			reply_markup=InlineKeyboard.TestMenu
		)
		pass
	# endregion ╰<If inline button>╯
	# region <If bot command>
	if type(call) is Message:
		# Якщо викликано через команду
		bot.send_message(
			chat_id=chat_id,
			text=GenerateMainMenuText(chat_type),
			reply_markup=InlineKeyboard.TestMenu
		)
	# endregion ╰<If bot command>╯
	pass

# endregion
# region /pin
def command_pin(message):
	"""
    Sends message with users chat id.
    """
	chat_id = message.chat.id
	out_msg = f'Your ID: <code>{chat_id}</code>'
	bot.reply_to(message, out_msg)
	pass
# endregion
# region /help
def command_help(message):
	"""
    Sends message with help text.
    """
	bot.send_message(message.from_user.id, 'BotHelpText')
	pass
# endregion
# region /test
def command_test(message):
	"""
    Handle /test command.

	:rtype:
    """
	chat_id = message.chat.id
	out_text = '<b>{}</b>\n{}'.format('Message:', jsonpickle.encode(message.json, unpicklable=False, indent=4))
	bot.send_message(chat_id, out_text, reply_markup=InlineKeyboard.TestMenu)
	pass
# endregion
# region /debug_message
def command_debug_message(message):
	"""Sends debug info message.

	:rtype:
    """
	chat_id = message.from_user.id
	out_text = f'Send me any message to get info about it.'
	bot.send_message(chat_id, out_text)

	# region [Debugging a message passed as a parameter]
	def ShowMessageDebugInfo(_message):
		splitted_text = util.split_string(jsonpickle.encode(_message, unpicklable=False, indent=4, separators=(',', ': ')), 3000)
		for text in splitted_text:
			bot.reply_to(_message, text)
		pass
	# endregion╰[Debugging a message passed as a parameter]╯
	bot.register_next_step_handler_by_chat_id(chat_id, ShowMessageDebugInfo)
	pass
# endregion
# region /delete_my_commands
def command_delete_my_commands(message):
	chat_id = message.from_user.id
	bot.delete_my_commands(scope=BotCommandScopeChat(chat_id), language_code='ru')
	pass
# endregion ╰─/delete_my_commands─╯

# endregion <General commands>

# endregion ╰───╼[Handle bot commands]╾───╯

# region ───╼[Handle callback query]╾───
@bot.callback_query_handler(func=lambda call: call.data == InlineKeyboard.EMTPY_FIELD)
def callback_empty_field_handler(call: CallbackQuery):
	bot.answer_callback_query(call.id, f"Callback from user: {call.message.from_user.full_name}", True)


def callback_query_handler(call):
	# region ──┨ VARIABLES ┠──
	chat_id = call.message.chat.id  # ID чата от которого пришел callback
	# call_data = call.data[3:]  # текст callback.data без "cb_" в начале
	# call_message = call.message                 # Сообщение от которого пришел callback
	# call_message_id = call.message.message_id  # ID сообщения от которого пришел callback
	# endregion

	# region ──┨ IF SHOW_CALLBACK_DATA is ON ┠──
	if SHOW_CALLBACK_DATA:
		bot.answer_callback_query(call.id, f'Callback: {call.data}')
		pass
	# endregion

	# region ──┨ BUTTONS HANDLERS ┠──

	# endregion

	pass


@bot.message_handler(chat_id=AllowedUsersIDs, commands=['template'])
@bot.callback_query_handler(func=lambda call: call.data == '/template')
def callback_teplate_handler(call: Union[CallbackQuery, Message]):
	# ToDo: Зробити перевірку наявності збереженого об'єкта шаблону

	# Якщо цей метод викликано через кнопку
	if type(call) is CallbackQuery:
		chat_id = call.message.chat.id
		user_id = call.message.from_user.id
		# Відповідаємо на отриманий callback
		bot.answer_callback_query(call.id, 'Налаштування шаблону скарбів')
		# Міняємо текст на кнопки повідомлення
		bot.edit_message_text(
			text=f'<code>⠀⠀⠀⠀⠀</code><b>Налаштування шаблону</b><code>⠀⠀⠀⠀⠀</code>\nЧерез кнопку',
			chat_id=chat_id,
			message_id=call.message.message_id,
			reply_markup=InlineKeyboard.TemplateMenu()
		)
	# Якщо цей метод викликано через команду
	else:
		chat_id = call.chat.id
		user_id = call.from_user.id
		# Відправляємо повідомлення з інфою об'єкта нового скарбу
		bot.send_message(
			chat_id,
			f'<code>⠀⠀⠀⠀⠀</code><b>Налаштування шаблону</b><code>⠀⠀⠀⠀⠀</code>\nЧерез команду',
			reply_markup=InlineKeyboard.TemplateMenu()
		)
	pass


# noinspection PyTypeChecker
@bot.message_handler(chat_id=AllowedUsersIDs, commands=['save_template'])
@bot.callback_query_handler(func=lambda call: call.data == '/save_template')
def callback_save_template_handler(call: Union[CallbackQuery, Message]):
	# Якщо цей метод викликано через кнопку
	if type(call) is CallbackQuery:
		chat_id = call.message.chat.id
		user_id = call.message.from_user.id
		# Відповідаємо на отриманий callback
		bot.answer_callback_query(call.id, 'Шаблон для скарбів Збережено!', show_alert=True)
		# Міняємо текст на кнопки повідомлення
		bot.edit_message_text(
			text=f'<code>⠀⠀⠀⠀⠀</code><b>Головне меню</b><code>⠀⠀⠀⠀⠀</code>\n',
			chat_id=chat_id,
			message_id=call.message.message_id,
			reply_markup=InlineKeyboard.MainMenu()
		)
	# Якщо цей метод викликано через команду
	else:
		chat_id = call.chat.id
		user_id = call.from_user.id
# endregion ╰╼[Handle callback query]╾╯

# region ───╼[Handle messages by bot state]╾───

# endregion ╰[Handle messages by bot state]╯

# region ───╼[Methods]╾───
# region ───[Filter users by ID]───
def FilterUsersById(message):
	chat_id = message.from_user.id
	error_text = 'No no no, you are not allowed to use this bot!'
	bot.send_message(chat_id, error_text)
	pass
# endregion ╰[Filter users by ID]╯

# endregion╰[Methods]╯

# region ───╼[Register message handlers]╾───
def RegisterMessageHandlers():
	# region -<Bot commands>-
	bot.register_message_handler(command_pin, chat_id=AllowedUsersIDs, commands=['pin'])  # /pin executor
	bot.register_message_handler(command_help, chat_id=AllowedUsersIDs, commands=['help'])  # /help executor
	# bot.register_message_handler(command_test, chat_id=AllowedUsersIDs, commands=['test'])  # /test executor
	bot.register_message_handler(command_test, chat_id=AllowedGroupsID, commands=['test'])  # /test executor
	bot.register_message_handler(command_debug_message, chat_id=AllowedUsersIDs, commands=['debug_message'])  # /debug_message executor
	bot.register_message_handler(command_delete_my_commands, chat_id=AllowedUsersIDs, commands=['delete_my_commands'])  # /debug_message executor
	# endregion ╰—<Bot commands>—╯
	# region -<Callback query>-
	bot.register_callback_query_handler(callback_query_handler, func=lambda call: True)  # Callback query handler
	# endregion ╰—<Callback query>—╯
	pass
# endregion ╰[Register message handlers]╯

# region ───╼[Update Listener]╾───
def UpdateListener(messages):
	for message in messages:
		chat_id = message.from_user.id
		# region [Filter not allowed users]
		if chat_id not in AllowedUsersIDs: FilterUsersById(message)
		"Фільтрація доступу користування користувачів по їх UserID"
		# endregion ╰—[Filter not allowed users]—╯
		# region [TESTING]
		# print(jsonpickle.encode(message, indent=2, unpicklable=False))

		# print(f'chat type: {message.chat.type}\n'
		# 	  f'chat_id: {message.chat.id}')
		# for e in m.entities:
		# 	print(e.to_json())
		# endregion ╰—[TESTING]—╯
		pass
	pass
# endregion ╰[Update Listener]╯

# region ───╼[General Methods]╾───
# bot.enable_save_next_step_handlers(delay=2)
# bot.add_custom_filter(custom_filters.IsDigitFilter())  # Фильтрация текста сообщения по цифре
RegisterMessageHandlers()  # Регистрация обработчиков для сообщений
bot.set_update_listener(UpdateListener)
bot.add_custom_filter(custom_filters.StateFilter(bot))  # Добавление кастомных состояний бота
bot.add_custom_filter(custom_filters.ChatFilter())  # Фильтрация пользователей по ID
bot.infinity_polling(timeout=5, long_polling_timeout=5)  # Запуск бота
# endregion
