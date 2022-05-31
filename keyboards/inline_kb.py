from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from data_base import db


menu_cd = CallbackData('show_result', 'level', 'category', 'exercises', 'user_id', 'save', 'variable')


# функция устанавливает параметры по умолчанию, если они не были переданы
def make_callback_data(level, user_id='0', category='0', exercises='0', save='1', variable=''):
    return menu_cd.new(level=level, user_id=user_id, category=category, exercises=exercises, save=save, variable=variable)


# формуриюет инлайн кнопки первого уровня с категориями
async def categories_kb(save):
    curr_level = 0
    markup = InlineKeyboardMarkup()

    categories = await db.get_categories()
    for category in categories:
        butt_text = f'{category[0]}'
        data = make_callback_data(level=curr_level+1, category=category[1], save=save)

        markup.insert(
            InlineKeyboardButton(text=butt_text, callback_data=data)
        )

    return markup


# формуриюет инлайн кнопки второго уровня с упражнениями
async def sub_categories_kb(categories_id, save):
    curr_level = 1
    markup = InlineKeyboardMarkup(row_width=1)

    sub_categories = await db.get_sub_categories(categories_id)
    for category in sub_categories:
        butt_text = f'{category[1]}'
        data = make_callback_data(level=curr_level+1, category=category[0], exercises=category[2], save=save)

        markup.insert(
            InlineKeyboardButton(text=butt_text, callback_data=data)
        )

    return markup


async def variable_sub_categories_kb(categories_id, save, exercises_id):
    curr_level = 2
    markup = InlineKeyboardMarkup(row_width=1)

    butt_text = ['Прогресс за месяц', 'Последние результаты', 'Пргоресс за все время']
    for text in butt_text:
        data = make_callback_data(level=curr_level+1, category=categories_id, save=save, exercises=exercises_id, variable=text)

        markup.insert(
            InlineKeyboardButton(text=text, callback_data=data)
        )

    return markup
