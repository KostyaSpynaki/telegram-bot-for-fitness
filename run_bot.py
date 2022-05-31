from aiogram.utils import executor
from create_bot import dp
from data_base import db
from handlers import client, register, exercises_save


async def on_startup(_):
    print('bot is online')
    db.sql_start()


client.register_handlers_client(dp)
register.register_handlers_register_client(dp)
exercises_save.register_handlers_save_progress(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
