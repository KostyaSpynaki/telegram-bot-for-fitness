from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from data_base import db
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMClient(StatesGroup):
    name = State()
    weight = State()


'''Начало регистрации пользователя'''


async def cm_start(message: types.Message):
    user = await db.find_user(message.from_user.id)
    if user:
        await message.answer('Вы уже зарегистрированы')
    else:
        await FSMClient.name.set()
        await message.reply('Введите имя')


'''Отмена регистрации'''


#@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.delete()
    await message.answer('Регистрация отменина')
    await message.answer('Обращайся')


'''Ловим имя пользователя'''


#@dp.message_handler(state=FSMClient.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['name'] = message.text
        await FSMClient.next()
        await message.reply('Введите ваш текущий вес')


'''Ловим вес пользователя'''


#@dp.message_handler(state=FSMClient.weight)
async def load_weight(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['weight'] = float(message.text)
    await db.add_user(state)
    await state.finish()


'''Регистрация хендлеров'''


def register_handlers_register_client(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands='Регистрация', state=None)
    dp.register_message_handler(cancel_state, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(load_name, state=FSMClient.name)
    dp.register_message_handler(load_weight, state=FSMClient.weight)