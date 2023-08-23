import os
import logging
from dotenv import load_dotenv
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import CallbackQuery
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from constants import (
    URL,
    START_TEXT,
    START_BUTTON,
    SELFIE,
    HIGH_SCHOOL_PHOTO,
    GPT_VOICE,
    SELFIE_URL,
    HIGH_SCHOOL_PHOTO_URL,
)

# Конфигурация логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton(START_BUTTON, web_app=WebAppInfo(url=URL)))
    markup.add(types.KeyboardButton(GPT_VOICE))
    await message.answer(START_TEXT, reply_markup=markup)

    selfie_button = InlineKeyboardButton(SELFIE, callback_data="selfie")
    high_school_photo_button = InlineKeyboardButton(
        HIGH_SCHOOL_PHOTO, callback_data="high_school"
    )

    selfie_markup = InlineKeyboardMarkup().add(selfie_button, high_school_photo_button)
    await message.answer("Шедевры искусства. Пробуйте))", reply_markup=selfie_markup)


@dp.message_handler(lambda message: message.text == GPT_VOICE)
async def send_gpt_voice(message: types.Message):
    try:
        logger.info("Sending GPT voice...")
        with open("audio/voice_gpt.ogg", "rb") as audio_file:
            await bot.send_voice(message.from_user.id, audio_file)
            logger.info("GPT voice sent successfully")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        logger.info("Finished processing callback")


@dp.callback_query_handler(lambda c: c.data in ["selfie", "high_school"])
async def send_photo_callback(callback_query: CallbackQuery):
    photo_urls = {"selfie": SELFIE_URL, "high_school": HIGH_SCHOOL_PHOTO_URL}

    photo_caption = {
        "selfie": "Вот мое последнее селфи! 😊",
        "high_school": "Вот мое фото из старшей школы!",
    }

    data = callback_query.data
    if data in photo_urls:
        await bot.send_photo(
            callback_query.from_user.id, photo_urls[data], caption=photo_caption[data]
        )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
