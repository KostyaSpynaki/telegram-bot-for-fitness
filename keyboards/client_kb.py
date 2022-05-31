from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from data_base import db

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
start_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)


# async def categories():
#     cat = await db.get_categories()
#     for c in cat:
#         butt = KeyboardButton(f'/{c[0]}')
#         kb_client.row(butt)


save_data = KeyboardButton('/Внести_данные')
get_data = KeyboardButton('/Просмотр_данных')

start_kb.row(save_data, get_data)
# b1 = KeyboardButton('/Грудь')
# b2 = KeyboardButton('/Ноги')
# b3 = KeyboardButton('/Спина')
# b4 = KeyboardButton('/Руки')
# b5 = KeyboardButton('/Плечи')



