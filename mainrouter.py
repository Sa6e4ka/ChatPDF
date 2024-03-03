# Dd вВ
from aiogram import F, Router, Bot
from aiogram.filters import Command, or_f, StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup

from main import upload, chat

DOWNLOAD_DIR = 'downloads/'

# main router
mr = Router()

class Chat(StatesGroup):
    upload = State()
    chat = State()


@mr.message(StateFilter('*') , F.text == '/delete')
async def delete(mes: Message, state: FSMContext):
    await state.clear()
    await mes.answer('Чтобы загрузить еще один документ, тыкай сюда -> /upload')

@mr.message(StateFilter(None), CommandStart())
async def start(mes : Message):
    await mes.answer('Мануальчик!\n\nЕсли хочешь загрузить документ, введи команду /upload\n\nТы можешь бесконечно отправлять вопросы боту по документу\n\nЧтобы загрузить новый (не первый) документ, введи /delete, а затем загрузи то, что нужно!')

@mr.message(StateFilter(None), Command('upload'))
async def uploading(mes : Message, state: FSMContext):
    await mes.answer('Отправь файл с расширением PDF')
    await state.set_state(Chat.upload)

@mr.message(StateFilter(Chat.upload), F.document)
async def uploading_(mes : Message, state: FSMContext, bot : Bot):
    try: 
        file_id = mes.document.file_id
        file_name = mes.document.file_name
        file_path = f'{DOWNLOAD_DIR}{file_name}'
        await bot.download(file_id, file_path)
        Source_id = upload(path=file_path)
        await state.update_data(Source_id = Source_id)
        await state.set_state(Chat.chat)

        await mes.answer('Теперь введи вопрос, который тебя интересует касаемо этого документа')
    except:
        await mes.answer('Что-то пошло не так 🥶\n\nТык -> /upload')
        await state.clear()

@mr.message(StateFilter(Chat.chat), F.text)
async def chating(mes : Message, state: FSMContext):
    quest = mes.text
    state_data = await state.get_data()
    await mes.answer(text=f'{str(chat(Source_id=state_data['Source_id'], message=quest))}\n\nЕсли хочешь прекратить работу с этим документом, то введи /delete')




    