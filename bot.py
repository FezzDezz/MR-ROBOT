# -*- coding: utf-8 -*-
# region ───╼[Imports]╾───
import jsonpickle
from typing import Union

import telebot
from telebot import custom_filters
from telebot.types import BotCommandScopeChat, BotCommandScopeDefault, CallbackQuery, Message
from telebot import util
from telebot.handler_backends import State, StatesGroup  # States
from telebot.storage import StateMemoryStorage
from keyboa import Keyboa, Button

from Config import *
from Keyboard import InlineKeyboard
from Treasure import Treasure, Template
# endregion ╰─╼[Imports]╾─╯

# region ───╼[Global flags]╾───
SHOW_CALLBACK_DATA = True
MESSAGE_DEBUG = False
DEBUG_MODE = True
# endregion ╰───╼[Global flags]╾───╯

# region ───╼[Objects initialization]╾───
jsonpickle.set_encoder_options('json', ensure_ascii=False)

state_storage = StateMemoryStorage()  # ToDo: Прикрутить pickle storage
bot = telebot.TeleBot(Token, parse_mode="HTML", skip_pending=True, state_storage=state_storage)

TemplateTreasure = Template()
"""Об'єкт шаблону скарбу"""
# endregion ╰───╼[Objects initialization]╾───╯

# region ───╼[Global classes]╾───
class JsonParser:
	@staticmethod
	def dumps(obj, indent=2):
		return jsonpickle.encode(obj, unpicklable=False, indent=indent, separators=(',', ': '))
	pass
# endregion ───╼[Global classes]╾───


# region ───╼[States group]╾───
class BotDataStates(StatesGroup):
	set = State()
	get = State()
	pass
# endregion ╰───╼[States group]╾───╯

# region ───╼[Handle bot commands]╾───
# region <General commands>
# region /start
@bot.message_handler(chat_id=AllowedIDs, commands=['start'])
@bot.callback_query_handler(func=lambda call: call.data == '/start')
def command_start_handler(call: Union[CallbackQuery, Message]):
	# region <Змінні функції>
	chat_id = call.message.chat.id if type(call) is CallbackQuery else call.chat.id
	chat_type = call.message.chat.type if type(call) is CallbackQuery else call.chat.type
	user_name = call.from_user.first_name
	# endregion <Змінні функції>
	# region <Обробка та сворення тексту та клавіатури для меню>
	def GenerateMainMenuText(_chat_type):
		headerEmptySpaceAmount = 5
		template_text = "{}{}".format('<i><b>шаблон скарбу:</b></i> ', '❌' if not TemplateTreasure.IsSet else f'\n{TemplateTreasure.ToString}')
		text = '<code>{header_line}</code>\n' \
			   '<code>{empty}</code><b>{header_text}</b><code>{empty}</code>\n' \
			   '<code>{header_line}</code>\n' \
			   '{template_text}\n'.format(header_line='—' * (18 + headerEmptySpaceAmount * 2),
										  empty='⠀' * headerEmptySpaceAmount,
										  header_text='ГОЛОВНЕ МЕНЮ',
										  template_text=template_text)
		if _chat_type == 'supergroup':
			text = f"{text}" \
				   f"<code>{'—' * (16 + headerEmptySpaceAmount * 2)}\n</code>" \
				   f"<b>👤:</b><code> {user_name}\n</code>"
			return text
		return text
	def GenerateMenuKeyboard():
		# Buttons
		btn_edit_template = Button(button_data={'Шаблон': 'template'}, front_marker='/').button
		btn_add_treasure = Button(button_data={'Добавити скарб': 'treasure'}, front_marker='/new_').button
		# Markup
		menu = [
			btn_edit_template,
			btn_add_treasure
		]
		# Keyboard
		keyboard = Keyboa(items=menu, items_in_row=1, copy_text_to_callback=False).keyboard
		return keyboard
	# endregion <Обробка та сворення тексту та клавіатури для меню>
	# region <Якщо викликано через Inline кнопки>
	if type(call) is CallbackQuery:
		# Якщо викликано через кнопку
		bot.answer_callback_query(call.id, f'Головне меню')
		bot.edit_message_text(
			text=GenerateMainMenuText(chat_type),
			chat_id=chat_id,
			message_id=call.message.message_id,
			reply_markup=GenerateMenuKeyboard()
		)
		pass
	# endregion ╰<Якщо викликано через Inline кнопки>╯
	# region <Якщо викликано через команду>
	if type(call) is Message:
		bot.send_message(
			chat_id=chat_id,
			text=GenerateMainMenuText(chat_type),
			reply_markup=GenerateMenuKeyboard()
		)
	# endregion ╰<Якщо викликано через команду>╯
	pass
# endregion
# region /pin
def command_pin(message):
	chat_id = message.chat.id
	out_msg = f'Your ID: <code>{chat_id}</code>'
	bot.reply_to(message, out_msg)
	pass
# endregion
# region /help
def command_help(message):
	bot.send_message(message.chat.id, 'BotHelpText')
	pass
# endregion
# region /test
def command_test(message):
	"""
    Handle /test command.

	:rtype:
    """
	chat_id = message.chat.id
	out_text = f'Template is set: <b>{TemplateTreasure.IsSet}</b>'
	bot.send_message(chat_id, out_text, reply_markup=None)
	pass
# endregion
# region /debug_message
def command_debug_message(message):
	"""
	A link_ in citation style.

	.. _link: ./

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

# region <Template treasure commands>
@bot.message_handler(chat_id=AllowedIDs, commands=['template'])
@bot.callback_query_handler(func=lambda call: call.data == '/template')
def command_template_handler(call: Union[CallbackQuery, Message]):
	print(JsonParser.dumps(call))
	chat_id = call.message.chat.id if type(call) is CallbackQuery else call.chat.id
	chat_type = call.message.chat.type if type(call) is CallbackQuery else call.chat.id
	user_name = call.from_user.first_name
	# region <Обробка та сворення тексту меню та клавіатури>
	def GenerateMenuText(_chat_type):
		headerEmptySpaceAmount = 5
		text = '<code>{header_line}</code>\n' \
			   '<code>{empty}</code><b>{header_text}</b><code>{empty}</code>\n' \
			   '<code>{header_line}</code>\n' \
			   '{body}' \
			   '<code>{header_line}</code>\n' \
			   '⠀'.format(header_line='—' * (18 + headerEmptySpaceAmount * 2),
						  empty=EmptySymbol * headerEmptySpaceAmount,
						  header_text=f'ШАБЛОН СКАРБУ',
						  body=TemplateTreasure.ToString)
		# text = f'{text}{TemplateTreasure.ToString}<code>{"—" * (24 + headerEmptySpaceAmount * 2)}</code>'
		if _chat_type == 'supergroup':
			text = f"{text}\n" \
				   f"<b>👤:</b><code> {user_name}\n</code>"
		return text
	def GenerateMenuKeyboard():
		# Buttons
		btn_edit_product = Button(button_data={'Товар': 'product'}, front_marker='/template_edit=').button
		btn_edit_amount = Button(button_data={'Кількість': 'amount'}, front_marker='/template_edit=').button
		btn_edit_hide_type = Button(button_data={'Тип': 'hide_type'}, front_marker='/template_edit=').button
		btn_edit_iso_color = Button(button_data={'Колір ізо': 'iso_color'}, front_marker='/template_edit=').button
		btn_edit_district = Button(button_data={'Район': 'district'}, front_marker='/template_edit=').button
		btn_return = Button(button_data={'« Назад': '/start'}).button
		# Markup
		# menu = [
		# 	[btn_edit_product, btn_edit_hide_type],
		# 	[btn_edit_iso_color, btn_edit_district],
		# 	btn_return
		# ]
		edit_markup = [btn_edit_product, btn_edit_amount, btn_edit_hide_type, btn_edit_iso_color, btn_edit_district]
		# Keyboard
		keyboard_edit = Keyboa(items=edit_markup, items_in_row=2, front_marker='/template_edit=', copy_text_to_callback=False).keyboard
		keyboard_controls = Keyboa(items=[[btn_return], ]).keyboard

		return Keyboa.combine(keyboards=(keyboard_edit, keyboard_controls))
	# endregion <Обробка та сворення тексту меню та клавіатури>
	# region <Якщо викликано через Inline кнопки>
	if type(call) is CallbackQuery:
		# Відповідаємо на отриманий callback
		bot.answer_callback_query(call.id, 'Налаштування шаблону')
		# Міняємо текст на кнопки повідомлення
		bot.edit_message_text(
			text=f'{GenerateMenuText(chat_type)}',
			chat_id=chat_id,
			message_id=call.message.message_id,
			reply_markup=GenerateMenuKeyboard()
		)
		pass
	# endregion <Якщо викликано через Inline кнопки>
	# region <Якщо викликано через команду>
	if type(call) is Message:
		bot.send_message(
			chat_id=chat_id,
			text=f'{GenerateMenuText(chat_type)}',
			reply_markup=GenerateMenuKeyboard()
		)
	# endregion <Якщо викликано через команду>
	pass

@bot.callback_query_handler(func=lambda call: call.data.split('=', 1)[0] == '/template_edit')
def command_template_edit_handler(call: CallbackQuery):
	chat_id = call.message.chat.id
	chat_type = call.message.chat.type
	user_name = call.from_user.first_name
	# region <Обробка та сворення тексту меню та клавіатури>
	def GenerateMenuText(_chat_type):
		text = ''
		if call.data.split('=', 1)[1] == 'product':
			text = '<b>Обери товар:</b>'
			pass
		elif call.data.split('=', 1)[1] == 'amount':
			text = '<b>Обери кількість:</b>'
			pass
		elif call.data.split('=', 1)[1] == 'hide_type':
			text = '<b>Обери тип:</b>'
			pass
		elif call.data.split('=', 1)[1] == 'iso_color':
			text = '<b>Обери колір ізо:</b>'
			pass
		elif call.data.split('=', 1)[1] == 'district':
			text = '<b>Обери район:</b>'
			pass
		if _chat_type == 'supergroup':
			# text = f"{text}\n" \
			# 	   f"<b>👤:</b><code> {user_name}\n</code>"
			text = f"<b>{user_name}</b> {text}"
		return text
	def GenerateMenuKeyboard(item_to_edit):
		# Buttons
		btn_return = Button(button_data={'« Назад': '/template'}).button
		# Menus
		editing_menu = None
		items_in_row = 2
		if item_to_edit == 'product':
			editing_menu = list(Products)
			items_in_row = 2
		elif item_to_edit == 'amount':
			editing_menu = list(Weights)
			items_in_row = 4
		elif item_to_edit == 'hide_type':
			editing_menu = list(HideTypes)
			items_in_row = 3
		elif item_to_edit == 'iso_color':
			editing_menu = list(Colors)
			items_in_row = 4
		elif item_to_edit == 'district':
			editing_menu = list(Districts)
			items_in_row = 2
		# Keyboards
		keyboard = Keyboa(
			items=editing_menu,
			items_in_row=items_in_row,
			front_marker=f'/template_set_{item_to_edit}=').keyboard
		keyboard_controls = Keyboa(items=[[btn_return], ]).keyboard

		return Keyboa.combine(keyboards=(keyboard, keyboard_controls))
	# endregion <Обробка та сворення тексту меню та клавіатури>

	# Відповідаємо на отриманий callback
	bot.answer_callback_query(
		callback_query_id=call.id,
		text='Редагування {}'.format(
			'продукту' if call.data.split('=', 1)[1] == 'product' else
			'кількості' if call.data.split('=', 1)[1] == 'amount' else
			'типу' if call.data.split('=', 1)[1] == 'hide_type' else
			'кольору ізо' if call.data.split('=', 1)[1] == 'iso_color' else
			'району' if call.data.split('=', 1)[1] == 'district' else '')
	)
	# Міняємо текст на кнопки повідомлення
	bot.edit_message_text(
		text=GenerateMenuText(chat_type),
		chat_id=chat_id,
		message_id=call.message.message_id,
		reply_markup=GenerateMenuKeyboard(call.data.split('=', 1)[1])
	)
	pass

@bot.callback_query_handler(func=lambda call: call.data.split('=', 1)[0][0:13] == '/template_set')
def command_template_set_item_handler(call: CallbackQuery):
	chat_id = call.message.chat.id
	chat_type = call.message.chat.type
	user_name = call.from_user.first_name
	item_to_set = call.data.split('=', 1)[0][14:]
	callback_answer_text = 'Втановлено '

	recived_callback: CallbackQuery = call

	# region <Обробка та сворення тексту та клавіатури для меню>
	def GenerateMenuText(_chat_type):
		menu_text = ''
		headerEmptySpaceAmount = 1
		menu_text = '<code>{header_line}</code>\n' \
					'<code>{empty}</code><b>{header_text}</b><code>{empty}</code>\n' \
					'<code>{header_line}</code>\n'.format(header_line='—' * (24 + headerEmptySpaceAmount * 2),
														  empty='⠀' * headerEmptySpaceAmount,
														  header_text='НАЛАШТУВАННЯ ШАБЛОНУ')
		menu_text = f'{menu_text}{TemplateTreasure.ToString}<code>{"—" * (24 + headerEmptySpaceAmount * 2)}</code>'
		if _chat_type == 'supergroup':
			text = f"{menu_text}\n" \
				   f"<b>👤:</b><code> {user_name}\n</code>"
		return menu_text
	def GenerateMenuKeyboard():
		# Buttons
		btn_edit_product = Button(button_data={'Товар': 'product'}, front_marker='/template_edit=').button
		btn_edit_hide_type = Button(button_data={'Тип': 'hide_type'}, front_marker='/template_edit=').button
		btn_edit_iso_color = Button(button_data={'Колір ізо': 'iso_color'}, front_marker='/template_edit=').button
		btn_edit_district = Button(button_data={'Район': 'district'}, front_marker='/template_edit=').button
		btn_save = Button(button_data={'Зберегти собі': '/template_save'}).button
		btn_return = Button(button_data={'« Назад': '/start'}).button
		# Markup
		menu = [
			[btn_edit_product, btn_edit_hide_type],
			[btn_edit_iso_color, btn_edit_district],
			btn_save,
			btn_return
		]
		# Keyboard
		keyboard = Keyboa(items=menu, copy_text_to_callback=False).keyboard
		return keyboard
	# endregion <Обробка та сворення тексту та клавіатури для меню>
	# region <Встановлюємо змінні TemplateProduct відповідно вибраному пункту>
	if item_to_set == 'product':
		TemplateTreasure.product = call.data.split('=', 1)[1]
		callback_answer_text += f'продукт: {TemplateTreasure.product}'
	elif item_to_set == 'amount':
		TemplateTreasure.amount = call.data.split('=', 1)[1]
		callback_answer_text += f'кількість: {TemplateTreasure.amount}'
	elif item_to_set == 'hide_type':
		TemplateTreasure.hide_type = call.data.split('=', 1)[1]
		callback_answer_text += f'тип: {TemplateTreasure.hide_type}'
	elif item_to_set == 'iso_color':
		TemplateTreasure.iso_color = call.data.split('=', 1)[1]
		callback_answer_text += f'колір ізо: {TemplateTreasure.iso_color}'
	elif item_to_set == 'district':
		TemplateTreasure.district = call.data.split('=', 1)[1]
		callback_answer_text += f'район: {TemplateTreasure.district}'
		pass
	# Запам'ятовуємо юзера хто встановлював шаблон
	TemplateTreasure.owner_user = user_name
	# endregion ╰<Встановлюємо змінні TemplateProduct відповідно вибраному пункту>╯

	# Відповідаємо на отриманий callback
	bot.answer_callback_query(callback_query_id=call.id, text=callback_answer_text)
	# Міняємо текст на кнопки повідомлення
	# bot.edit_message_text(
	# 	text=f'{GenerateMenuText(chat_type)}',
	# 	chat_id=chat_id,
	# 	message_id=call.message.message_id,
	# 	reply_markup=GenerateMenuKeyboard()
	# )

	recived_callback.data = '/template'
	command_template_handler(recived_callback)
	pass

# endregion ╰<Template treasure commands>╯

# endregion ╰───╼[Handle bot commands]╾───╯

# region ───╼[Handle callback query]╾───
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
	bot.send_message(chat_id, call.data)
	pass

@bot.callback_query_handler(func=lambda call: call.data == '/save_template')
def callback_save_template_handler(call: CallbackQuery):
	# chat_id = call.message.chat.id
	# chat_type = call.message.chat.type
	# user_id = call.from_user.id
	# user_name = call.from_user.first_name
	# ToDo: Добавити тут зберігання шаблону
	command_start_handler(call)
	bot.answer_callback_query(call.id, 'Шаблон для скарбів Збережено!', show_alert=True)
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
	bot.register_message_handler(command_test, chat_id = [AllowedIDs], commands=['test'])  # /test executor
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
		if chat_id not in AllowedUsersIDs:
			"Фільтрація доступу користування користувачів по їх UserID"
			FilterUsersById(message)
		# endregion ╰—[Filter not allowed users]—╯
		# region [Message dubugging]
		if MESSAGE_DEBUG:
			# print(jsonpickle.encode(message, indent=2, unpicklable=False))
			print(JsonParser.dumps(message))
		# endregion ╰─[Message dubugging]─╯

		# region [TESTING]

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
