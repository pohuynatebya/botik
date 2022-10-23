from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hlink
from aiogram.dispatcher.filters import Text
import re
import logging

TOKEN = "5680571181:AAHPgvLhbEtGKXSL9DX0yTtdIx_cJWDcmdU"
OWNER = '-813072413'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

def get_menu(menu_name):
	match menu_name:
		case 'startmenu':
			buttons = [
				types.InlineKeyboardButton(text='⭐️Owner', url='https://t.me/kamolgks'),
				types.InlineKeyboardButton(text='☕️Github', url='t.me/kamolgks'),
				types.InlineKeyboardButton(text='🌒Website <3', url='https://kamolgks.ml'),
				]
		case 'nometamenu':
			buttons = [
			    types.InlineKeyboardButton(text='😶‍🌫️More', url='https://t.me/NoMetaPlse'),
			    ]
			
	keyboard = types.InlineKeyboardMarkup(row_width=2)
	keyboard.add(*buttons)
	return keyboard

@dp.message_handler(commands='start')
async def process_start(message: types.Message):
	await message.answer_video(video='https://te.legra.ph/file/188145d8da10975137e94.mp4', caption='🪄 Welcome to my feedback bot, You may contact with me\n▫️Write your message and my host will answer you!\n▫️Please read /nometa', reply_markup=get_menu('startmenu'))

@dp.message_handler(commands='nometa')
async def process_nometa(message: types.Message):
	await message.answer("👨‍🎓 Internet-talk rules:\n\n🚫 Do not send just 'Hello\n🚫 Do not advertise\n🚫 Do not insult\n🚫 Do not split message\n✅ Write your question in one message", reply_markup=get_menu('nometamenu'))

@dp.message_handler()
async def messages(message: types.Message):
	if str(message.chat.id) == OWNER:
		if message.reply_to_message:
			try:
				message_data = message.reply_to_message.text
				original_user_id = re.findall('UID: [0-9]+', message_data)[0].replace('UID: ', '').strip()
				original_message_id = re.findall('MID: [0-9]+', message_data)[0].replace('MID: ', '').strip()
				await bot.send_message(original_user_id, message.text, reply_to_message_id=original_message_id, allow_sending_without_reply=True)
				text = f'The message was sent to the user with ID: {original_user_id}'
				await bot.send_message(OWNER, text)
			except Exception as ex:
				print(ex)
	else:
		try:
			await bot.send_message(OWNER, f'<b>Message from {hlink(message.from_user.first_name, "tg://user?id=" + str(message.from_user.id))} (UID: {message.from_user.id}, MID: {message.message_id})</b> \n\nMessage: {message.text}')
			await bot.send_message(message.chat.id, f'✅{message.from_user.first_name}, your message has been received.')
		except Exception as ex:
			print(ex)


if __name__ == '__main__':
	executor.start_polling(dp)