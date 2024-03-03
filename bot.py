#Импортируем нужные дополнительные модули
import os
import asyncio


# Импортируем нужные модули из aiogram
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import BotCommandScopeAllPrivateChats, Message
from aiogram.client.default import DefaultBotProperties

from commands import private

#Достаем токен бота и url базы данных из переменной окружения
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from mainrouter import mr


#Создаем объект бота (передаем ему режим парсига получаемых ответов)
bot= Bot(token=os.getenv('BOT_TOKEN'), default=DefaultBotProperties(parse_mode='HTML'))
#Создаем объект диспетчера
dp = Dispatcher()

dp.include_router(mr)

# Добавляем основные "глобальные" хендлеры
@dp.message(Command('state'))
async def state_get(message: Message, state: FSMContext):
    current_state = await state.get_state()
    await message.answer(
        text=f'Текущее состояние: {current_state}'
    )


# Команда очистки состояния
@dp.message(Command('stateclear'))
async def clear_state(message: Message, state: FSMContext):
    current_state = await state.get_state()
    await state.clear()
    clear_state = await state.get_state()
    await message.answer(f'Состояние <b>{current_state}</b> сменилось на <b>{clear_state}</b>')


#Запускаем бота, помещаем доступные апдейты в start_polling
# отключаем обработку незавершившихся запросов
# Подключаем базу данных
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private,scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot,allowed_updates=dp.resolve_used_update_types())

# Запуск main
if __name__ == "__main__":
    try:   
        print("I'M ALIVE BIIIYYYAAAATCH")
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот остановлен!')
        pass
    except Exception as e:  
       print(f'КРИТИЧЕСКАЯ ОШИБКА: {e}')