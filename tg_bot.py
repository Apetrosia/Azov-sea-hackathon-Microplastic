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

area_set = False
height, width = 0, 0

# Обработка команды \start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Для начала работы отправьте фото, на котором нужно обнаружить микропластик. "
                         f"Сначала отправьте высоту и ширину картинки через пробел.")

@dp.message(F.text)
async def save_area_value(message: Message):
    global area_set
    global height, width
    try:
        area_set = True
        height, width = map(int, message.text.split())
        await message.answer(text="Площадь задана. Можете отправить изображение")
    except:
        await message.answer(text="Неверный формат площади!")

# Обработка начала опроса
@dp.message(F.photo)
async def download_photo(message: Message, bot: Bot):
    global area_set
    if not area_set:
        await message.answer("Площадь не была указана! Фото не будет обработано")
        return
    image_path = f"tmp/{message.photo[-1].file_id}.png"
    res_path = f"tmp/"
    res_name = f"tmp/result_{message.photo[-1].file_id}.png"
    await bot.download(message.photo[-1], destination=image_path)
    await message.answer("Результаты вычисляются...")
    image = find_microplastic.open_image(image_path)
    boxes, indices, confidences = find_microplastic.detect_microplastics(image)
    info, areas = find_microplastic.draw_bounds(image, boxes, indices, confidences)
    find_microplastic.save_image(image, image_path, res_path)
    photo = FSInputFile(res_name)
    await message.answer_photo(photo=photo)
    await message.answer(text=f"Количество обнаруженных частиц: {len(info)}")
    template = '{:.' + str(6) + 'f}'
    for i in range(len(info)):
        particle = info[i] #{areas[i][0] * height}\n
        particle += f"Высота: " + template.format(areas[i][0] * height) + "\n" \
                    f"Ширина: " + template.format(areas[i][1] * width) + "\n" # {areas[i][1] * width}\n"
        await message.answer(text=particle + "\n")
    os.remove(image_path)
    os.remove(res_name)
    area_set = False

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
