from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, filters
from aiogram.utils import executor
import random
import conf
import time
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards.keyboadrs import keyb_main, keyb_st
from loguru import logger
from aiogram.utils.executor import start_webhook
from aiogram.dispatcher.filters.state import State, StatesGroup

DEV_MODE = False
##------------------Блок ініціалізації-----------------##
API_Token = conf.TOKEN
ADMIN_ID = conf.ADMIN_ID
bot = Bot(token=API_Token)
logger.add("debug.txt")
# webhook settings
WEBHOOK_HOST = 'https://vmi957205.contaboserver.net'
WEBHOOK_PATH = '/prod_game'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'  # or ip 127.0.0.1
WEBAPP_PORT = 3011
bot = Bot(token=API_Token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

x = 0
count = 0


class FSMdig(StatesGroup):
    dig = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Вітаю! Обери ігру ⬇️", reply_markup=keyb_main)

@dp.message_handler(filters.Text(startswith="Камінь🪨 ножиці✂️ бумага📜"))
async def foots(message: types.Message):
    await message.answer("Вибери: ", reply_markup=keyb_st)

@dp.message_handler(filters.Text(startswith="Вгадай число"), state=None)
async def foots(message: types.Message):
    global x, count
    x = random.randrange(100)
    count = 0
    await FSMdig.dig.set()
    print("Input digit from 0 to 100")
    await message.answer("Я загадав число X від 1 до 100, спробуй його вгадати.\nВведи число:")


@dp.message_handler(content_types=[types.ContentType.TEXT], state=FSMdig.dig)
async def foots(message: types.Message, state: FSMdig):
    global x, count
    num = message.text
    if num.isdigit():
        num = int(num)
        count += 1
        if num > x:
            print("Lover")
            await message.answer("Число Х менше ⬇️")
        if num < x:
            print("Hier")
            await message.answer("Число Х більше ⬆️")
        if num == x:
            print(f"You win! in {count} count")
            await message.answer(f"You win!🥇🏆 in {count} count", reply_markup=keyb_main)
            count = 0
            await state.finish()
    else:
        print("Input digit 🔢 please!")

@dp.message_handler()
async def foots(message: types.Message, state: FSMdig):
    await message.answer("Обери ігру ⬇️", reply_markup=keyb_main)

@dp.callback_query_handler()
async def change_image_callback(query: types.CallbackQuery):
    await bot.send_chat_action(chat_id=query.message.chat.id, action="typing")
    time.sleep(1)
    bot_ch = random.choice(("stone", "paper", "cross"))
    usr_ch = query.data
    if bot_ch == usr_ch :
        await bot.send_message(chat_id=query.message.chat.id,text = f"Я - {bot_ch} ти - {usr_ch} Нічия! Спробуй ще раз")
        await bot.send_message(chat_id=query.message.chat.id, text=f"Вибери: ", reply_markup=keyb_st)

    if bot_ch == 'stone' and usr_ch == 'paper':
        await bot.send_message(chat_id=query.message.chat.id, text=f"Я - 🪨 ти - 📜 ти переміг!🏆")
        await bot.send_message(chat_id=query.message.chat.id, text=f"Вибери: ", reply_markup=keyb_st)
    if bot_ch == 'stone' and usr_ch == 'cross':
        await bot.send_message(chat_id=query.message.chat.id, text=f"Я - 🪨 ти - ✂️ ти програв!")
        await bot.send_message(chat_id=query.message.chat.id, text=f"Вибери: ", reply_markup=keyb_st)

    if bot_ch == 'paper' and usr_ch == 'cross':
        await bot.send_message(chat_id=query.message.chat.id, text=f"Я - 📜 ти - ✂️ ти переміг!🏆")
        await bot.send_message(chat_id=query.message.chat.id, text=f"Вибери: ", reply_markup=keyb_st)
    if bot_ch == 'paper' and usr_ch == 'stone':
        await bot.send_message(chat_id=query.message.chat.id, text=f"Я - 📜 ти - 🪨 ти програв!")
        await bot.send_message(chat_id=query.message.chat.id, text=f"Вибери: ", reply_markup=keyb_st)

    if bot_ch == 'cross' and usr_ch == 'paper':
        await bot.send_message(chat_id=query.message.chat.id, text=f"Я - ✂️ ти - 📜 ти програв!")
        await bot.send_message(chat_id=query.message.chat.id, text=f"Вибери: ", reply_markup=keyb_st)
    if bot_ch == 'cross' and usr_ch == 'stone':
        await bot.send_message(chat_id=query.message.chat.id, text=f"Я - ✂️ ти - 🪨 ти переміг!🏆")
        await bot.send_message(chat_id=query.message.chat.id, text=f"Вибери: ", reply_markup=keyb_st)



##-------------------Запуск бота-------------------------##
if DEV_MODE:
    print("Bot running")
    executor.start_polling(dp, skip_updates=True)
else:
    async def on_startup(dp):
        await bot.set_webhook(WEBHOOK_URL)
        logger.debug("Бот запущено")

    async def on_shutdown(dp):
        logger.debug('Зупиняюся...')
        await bot.delete_webhook()
        await dp.storage.close()
        await dp.storage.wait_closed()

    if __name__ == '__main__':
       # dp.middleware.setup(MidlWare())
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )


