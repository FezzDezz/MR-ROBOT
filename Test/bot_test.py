# -*- coding: utf-8 -*-
import re

import telebot  # telebot
from telebot.types import *

from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup  # States

# States storage
from telebot.storage import StateMemoryStorage

# Starting from version 4.4.0+, we support storages.
# StateRedisStorage -> Redis-based storage.
# StatePickleStorage -> Pickle-based storage.
# For redis, you will need to install redis.
# Pass host, db, password, or anything else,
# if you need to change config for redis.
# Pickle requires path. Default path is in folder .state-saves.
# If you were using older version of pytba for pickle,
# you need to migrate from old pickle to new by using
# StatePickleStorage().convert_old_to_new()


# Now, you can pass storage to bot.
state_storage = StateMemoryStorage()  # you can init here another storage

bot = telebot.TeleBot("5375930227:AAHuCEV2VWy9pBwrUZ_2pmVrErRZuu7iD3I", state_storage=state_storage)


# States group.
class MyStates(StatesGroup):
	# Just name variables differently
	name = State()  # creating instances of State class is enough from now
	group_name = State()  # creating instances of State class is enough from now
	surname = State()
	age = State()


def is_command(text: str) -> bool:
	"""Checks if `text` is a command. Telegram chat commands start with the '/' character.

	:param text: Text to check.
	:return: True if `text` is a command, else False.
	"""
	if text is None: return False
	return text.startswith('/')


def extract_arguments(text):
	regexp = re.compile(r"/\w*(@\w*)*\s*([\s\S]*)", re.IGNORECASE)
	result = regexp.match(text)
	g = result.groups()
	print(g[0])
	return result.group(2) if (is_command(text) and result.groups()[0] == '') else g[0]


@bot.message_handler(commands=['start'])
def start_ex(message):
	bot.send_message(message.chat.id, 'Hi, write me a surname')
	bot.register_next_step_handler_by_chat_id(message.chat.id, TestStepHandler, needed_user=message.from_user.id)

def TestStepHandler(message, **kwargs):
	if kwargs['needed_user'] != message.from_user.id:
		bot.register_next_step_handler_by_chat_id(message.chat.id, TestStepHandler, needed_user=kwargs['needed_user'])
		bot.send_message(message.chat.id, f'Got wrong user! user_id: {message.from_user.id}')
	else:
		bot.send_message(message.chat.id, f'Gotcha!')

@bot.message_handler(state=MyStates.surname)
def ask_age(message):
	"""
	State 2. Will process when user's state is MyStates.surname.
	"""
	bot.send_message(message.chat.id, "What is your age?")
	bot.set_state(message.from_user.id, MyStates.age, message.chat.id)
	with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
		data['surname'] = message.text







	"""
	Start command. Here we are starting state
	"""
	# try:
	# 	b = message.text.split('@', 1)
	# 	print(b)
	# except Exception as e:
	# 	print(f'Exception: {e}')
	#
	# a = extract_arguments(message.text)
# 	# print("args:", a)
#
# def TestStepHandler(message):
# 	bot.send_message(message.chat.id, f'Got user_id: {message.from_user.id}')
# 		bot.send_message(message.chat.id, f"args:")
# 		for a in args:
# 			bot.send_message(message.chat.id, f"Argument-->{a}")
# 		bot.send_message(message.chat.id, f"kwargs:")
# 		for k, v in user.items():
# 			bot.send_message(message.chat.id, f"Key:{k}-->Value:{v}")
# 	# if message.from_user.id == _user_id:
# 	# 	bot.send_message(message.chat.id, f"GOTCHA!")
# 	# else:
# 	# 	bot.send_message(message.chat.id, f"NO NO NO!")

# Any state
@bot.message_handler(state='*', commands=['cancel'])
def any_state(message):
	"""
	Cancel state
	"""
	bot.delete_state(message.from_user.id)
	bot.send_message(message.chat.id, f"State: {bot.get_state(message.from_user.id)}")
	bot.send_message(message.chat.id, "Your state was cancelled.")


# noinspection PyUnresolvedReferences
@bot.message_handler(state=MyStates.name)
def name_get(message):
	"""
	State 1. Will process when user's state is MyStates.name.
	"""
	bot.send_message(message.chat.id, f'Now write me a surname')
	bot.set_state(message.from_user.id, MyStates.surname)
	with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
		data['name'] = message.text


@bot.message_handler(state=MyStates.surname)
def ask_age(message):
	"""
	State 2. Will process when user's state is MyStates.surname.
	"""
	bot.send_message(message.chat.id, "What is your age?")
	bot.set_state(message.from_user.id, MyStates.age, message.chat.id)
	with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
		data['surname'] = message.text


# result
@bot.message_handler(state=MyStates.age, is_digit=True)
def ready_for_answer(message):
	"""
	State 3. Will process when user's state is MyStates.age.
	"""
	with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
		data_text = ''
		for k, v in data.items():
			data_text += f"key:{k}----value:{v}\n"
		print(data_text)
		bot.send_message(message.chat.id,
						 "Ready, take a look:\n<b>Name: {name}\nSurname: {surname}\nAge: {age}</b>".format(name=data['name'], surname=data['surname'],
																										   age=message.text), parse_mode="html")
	bot.delete_state(message.from_user.id, message.chat.id)


# incorrect number
@bot.message_handler(state=MyStates.age, is_digit=False)
def age_incorrect(message):
	"""
	Wrong response for MyStates.age
	"""
	bot.send_message(message.chat.id, 'Looks like you are submitting a string in the field age. Please enter a number')


# region ───╼[Update Listener]╾───
def UpdateListener(messages):
	for message in messages:
		user_id = message.from_user.id
		chat_id = message.chat.id
		# if chat_id == -1001689943810:
		# 	text = f"-----Bot state: '{bot.get_state(user_id, chat_id)}'-----\n" \
		# 		   f"UserID: '{user_id}'\n" \
		# 		   f"ChatID: '{chat_id}'\n" \
		# 		   f"Text: '{message.text}'\n" \
		# 		   f"------------------------------------"
		# 	print(text)
		# 	bot.send_message(chat_id, text)
		# 	if bot.get_state(user_id, chat_id) == MyStates.name:
		# 		print('text')
		# 		name_get(message)
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


# register filters
bot.set_update_listener(UpdateListener)
bot.add_custom_filter(custom_filters.ChatFilter())
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())

bot.infinity_polling(skip_pending=True)
