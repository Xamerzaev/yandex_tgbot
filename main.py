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
    GITHUB_URL,
    START_TEXT,
    START_BUTTON,
    SELFIE,
    HIGH_SCHOOL_PHOTO,
    GPT_VOICE,
    SELFIE_URL,
    HIGH_SCHOOL_PHOTO_URL,
    SQL_NOSQL_VOICE,
    FISRT_LOVE_VOICE,
)

# Конфигурация логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Получение токена бота из .env файла
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Создание экземпляров бота и хранилища
bot = Bot(token=TELEGRAM_BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

# Список меток для кнопок
button_labels = [GPT_VOICE, SQL_NOSQL_VOICE, FISRT_LOVE_VOICE]


# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    """
    Обработчик команды /start.

    Args:
        message (types.Message): Входящее сообщение.

    Returns:
        None
    """
    # Создание клавиатуры с кнопками
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton(START_BUTTON, web_app=WebAppInfo(url=GITHUB_URL)))
    buttons = [types.KeyboardButton(label) for label in button_labels]
    markup.add(*buttons)

    # Отправка стартового сообщения с клавиатурой
    await message.answer(START_TEXT, reply_markup=markup)

    # Создание кнопок для инлайн-клавиатуры
    selfie_button = InlineKeyboardButton(SELFIE, callback_data="selfie")
    high_school_photo_button = InlineKeyboardButton(
        HIGH_SCHOOL_PHOTO, callback_data="high_school"
    )
    selfie_markup = InlineKeyboardMarkup().add(selfie_button, high_school_photo_button)

    # Отправка сообщения с инлайн-клавиатурой
    await message.answer("Шедевры искусства. Пробуйте))", reply_markup=selfie_markup)


# Функция для отправки голосовых сообщений с логированием
async def send_voice_with_logging_async(chat_id, audio_filename, log_message):
    """
    Отправка голосовых сообщений с логированием.

    Args:
        chat_id: Идентификатор чата.
        audio_filename: Путь к аудио файлу.
        log_message: Сообщение для логирования.

    Returns:
        None
    """
    try:
        logger.info(f"Sending {log_message} voice...")
        with open(audio_filename, "rb") as audio_file:
            await bot.send_voice(chat_id, audio_file)
            logger.info(f"{log_message} voice sent successfully")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        logger.info("Finished processing callback")


# Обработчик текстовых сообщений для отправки голосовых сообщений
@dp.message_handler(
    lambda message: message.text in [FISRT_LOVE_VOICE, SQL_NOSQL_VOICE, GPT_VOICE]
)
async def send_voice(message: types.Message):
    """
    Обработчик текстовых сообщений для отправки голосовых сообщений.

    Args:
        message (types.Message): Входящее сообщение.

    Returns:
        None
    """
    chat_id = message.from_user.id
    if message.text == FISRT_LOVE_VOICE:
        await send_voice_with_logging_async(
            chat_id, "audio/first_love.ogg", "first love"
        )
    elif message.text == SQL_NOSQL_VOICE:
        await send_voice_with_logging_async(chat_id, "audio/sql_nosql.ogg", "SQL/NOSQL")
    elif message.text == GPT_VOICE:
        await send_voice_with_logging_async(chat_id, "audio/voice_gpt.ogg", "GPT")


# Обработчик инлайн-клавиатуры для отправки фото
@dp.callback_query_handler(lambda c: c.data in ["selfie", "high_school"])
async def send_photo_callback(callback_query: CallbackQuery):
    """
    Обработчик инлайн-клавиатуры для отправки фото.

    Args:
        callback_query (CallbackQuery): Инлайн-клавиатура.

    Returns:
        None
    """
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


# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
