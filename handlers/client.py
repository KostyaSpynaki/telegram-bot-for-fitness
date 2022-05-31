from typing import Union
from aiogram import types, Dispatcher
from handlers import other, exercises_save
from create_bot import dp
from data_base import db
from keyboards import kb_client, client_kb, start_kb, inline_kb
from keyboards.inline_kb import menu_cd


'''Команда старт'''


#@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    user = await db.find_user(message.from_user.id)
    if user:
        await message.answer('Здравствуйте', reply_markup=start_kb)
    else:
        await message.answer('Зарегистрируйтесь')


# '''Получение данных по категориям'''
#
#
# async def command_get_categories(message: types.Message):
#     await client_kb.categories()
#     await message.answer('Выберите категорию', reply_markup=kb_client)
#
#
# '''Получение данных по категориям'''
#
#
# async def command_put_categories(message: types.Message):
#     await client_kb.categories()
#     await message.answer('Выберите категорию', reply_markup=kb_client)


# async def load_progresss(message: types.Message):
#     us_id = int(message.from_user.id)
#     progress = await db.select_progress(message.text.strip('/'), us_id)
#     progress_user = other.parse(progress)
#     await message.answer(progress_user)


'''Инлайн кнопки с категориями'''


async def get_categories(message: Union[types.Message, types.CallbackQuery], **kwargs):
    if str(message.get_command()) == '/Внести_данные':
        save = '0'
    else:
        save = '1'
    markup = await inline_kb.categories_kb(save)
    await message.answer('Выберите категорию', reply_markup=markup)


'''Инлайн кнопки с упражнениями'''


async def get_sub_categories(callback: types.CallbackQuery, categories, save, **kwargs):
    markup = await inline_kb.sub_categories_kb(categories, save)
    await callback.message.edit_reply_markup(markup)
    await callback.answer('Выберите упражнение')


async def get_variable_sub_categories(callback: types.CallbackQuery, categories, save, exercises, **kwargs):
    markup = await inline_kb.variable_sub_categories_kb(categories, save, exercises)
    await callback.message.edit_reply_markup(markup)


'''Выводит прогресс пользователя за все время'''


async def load_progress(callback: types.CallbackQuery, variable, categories, exercises, **kwargs):
    us_id = int(callback.from_user.id)
    if variable == 'Последние результаты':
        progress = await db.get_progress_user_last(exercises, us_id)
    elif variable == 'Прогресс за месяц':
        progress = await db.get_progress_user_month(exercises, us_id)
    else:
        progress = await db.get_progress(exercises, us_id)
    progress_user = other.parse(progress)
    await callback.message.answer(progress_user)


# '''Выводит последний введенный прогресс пользователя'''
#
#
# async def last_progress_user(callback: types.CallbackQuery, categories, exercises, **kwargs):
#     us_id = int(callback.from_user.id)
#     progress = await db.get_progress_user_last(exercises, us_id)
#     progress_user = other.parse(progress)
#     await callback.message.answer(progress_user)
#
#
# '''Выводит прогресс пользователя за последний месяц'''
#
#
# async def month_progress_user(callback: types.CallbackQuery, categories, exercises, **kwargs):
#     us_id = int(callback.from_user.id)
#     progress = await db.get_progress_user_last(exercises, us_id)
#     progress_user = other.parse(progress)
#     await callback.message.answer(progress_user)


"""При нажатии на инлайн кнопку запускаем нужную функцию"""


@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: types.CallbackQuery, callback_data: dict):
    curr_level = callback_data.get('level')
    category = callback_data.get('category')
    sub_category = callback_data.get('exercises')
    use_id = callback_data.get('user_id')
    save = callback_data.get('save')
    variable = callback_data.get('variable')

    # создаем словарь с уровнем вложенности инлайн кнопок и вызываем соотв. функцию
    levels = {
        '1': get_sub_categories,
        '2': get_variable_sub_categories,
        '3': load_progress,
    }

    # флаг save, при котором меням функцию вывода прогресса, на ввод
    if save == '0':
        levels['2'] = exercises_save.cm_start_save
        del levels['3']

    # if variable == 'Последние результаты':
    #     levels['3'] = last_progress_user
    #
    # if variable == 'Прогресс за месяц':
    #     levels['3'] = month_progress_user

    curr_level_func = levels[curr_level]
    await curr_level_func(
        call,
        categories=category,
        exercises=sub_category,
        user_id=use_id,
        variable=variable,
        save=save
    )


'''Регистрация хендлеров'''


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands='start')
    dp.register_message_handler(get_categories, commands='Просмотр_данных')
    dp.register_message_handler(get_categories, commands='Внести_данные')
    #dp.register_message_handler(command_get_categories, commands=['Просмотр_данных',])
    #dp.register_message_handler(load_progress, commands=['Грудь', 'Ноги', 'Спина', 'Плечи', 'Руки'])



