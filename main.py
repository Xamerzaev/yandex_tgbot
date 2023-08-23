import os
from dotenv import load_dotenv
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import CallbackQuery
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
URL = 'https://xamerzaev.github.io/DikNus/'
START_TEXT = 'Добро пожаловать!'
START_BUTTON = 'Что-то не по ТЗ :)'
SELFIE = 'Посмотреть последнее селфи разработчика'

bot = Bot(token=TELEGRAM_BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton(START_BUTTON, web_app=WebAppInfo(url=URL)))
    await message.answer(START_TEXT, reply_markup=markup)

    selfie_button = InlineKeyboardButton(text="Посмотрите последнее селфи разработчика:", callback_data="selfie")
    selfie_markup = InlineKeyboardMarkup().add(selfie_button)
    await message.answer("Шедевры искусства. Пробуйте))", reply_markup=selfie_markup)

@dp.callback_query_handler(lambda c: c.data == "selfie")
async def send_selfie(callback_query: CallbackQuery):
    selfie_url = 'https://imageup.ru/img109/4489967/img_2923.jpg'

    await bot.send_photo(callback_query.from_user.id, selfie_url, caption="Вот мое последнее селфи! 😊")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
