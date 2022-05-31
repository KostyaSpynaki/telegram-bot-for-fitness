from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from data_base import db
from aiogram.dispatcher.filters.state import State, StatesGroup
import time


class FSMClientExercisesSave(StatesGroup):
    repeats = State()
    weight = State()


'''Начало состояния сохранения прогресса'''


async def cm_start_save(callback: types.CallbackQuery, categories, exercises, **kwargs,):
    global exercise
    exercise = exercises
    await FSMClientExercisesSave.repeats.set()
    await callback.message.answer('Введите вес')


'''Отмена сохранения в бд'''


#@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.delete()
    await message.answer('Сохранение отменино')
    await message.answer('Обращайся')


'''Ловим вес упражнения пользователя'''


#@dp.message_handler(state=FSMClient.name)
async def load_repeats(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data['use_id'] = message.from_user.id
            data['exerc_id'] = exercise
            data['weight'] = float(message.text)
            await FSMClientExercisesSave.next()
            await message.reply('Введите кол-во повторов')
    else:
        await message.answer('Введите число\n'
                             'Или напишите <отмена>, что бы отменить сохранение')


'''Ловим кол-во повторов'''


#@dp.message_handler(state=FSMClient.weight)
async def load_weight(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data['repeats'] = float(message.text)
            data['date'] = str(time.time())
        await db.save_users_exercises(state)
        await state.finish()
        await message.answer('Успешно!')
    else:
        await message.answer('Введите число\n'
                             'Или напишите <отмена>, что бы отменить сохранение')


'''Регистрация хендлеров'''


def register_handlers_save_progress(dp: Dispatcher):
    dp.register_message_handler(cancel_state, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(load_repeats, state=FSMClientExercisesSave.repeats)
    dp.register_message_handler(load_weight, state=FSMClientExercisesSave.weight)