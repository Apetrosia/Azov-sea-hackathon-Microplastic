import os

import find_microplastic
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, FSInputFile
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, StateFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hbold

# Токен бота
TOKEN = "6597199456:AAGfbAsSCcEVArI5qhYuENidHDjwNogvyhE"
dp = Dispatcher(storage=MemoryStorage())

# Обработка команды \start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Для начала работы отправьте фото, на котором нужно обнаружить микропластик.")

# Обработка начала опроса
@dp.message(F.photo)
async def download_photo(message: Message, bot: Bot):
    image_path = f"tmp/{message.photo[-1].file_id}.png"
    res_path = f"tmp/"
    res_name = f"tmp/result_{message.photo[-1].file_id}.png"
    await bot.download(message.photo[-1], destination=image_path)
    await message.answer("Результаты вычисляются...")
    image = find_microplastic.open_image(image_path)
    boxes, indices, confidences = find_microplastic.detect_microplastics(image)
    info = find_microplastic.draw_bounds(image, boxes, indices, confidences)
    find_microplastic.save_image(image, image_path, res_path)
    photo = FSInputFile(res_name)
    await message.answer_photo(photo=photo)
    for particle in info:
        await message.answer(text=particle)
    os.remove(image_path)
    os.remove(res_name)

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
