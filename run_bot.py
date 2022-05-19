from aiogram.utils import executor
from create_bot import dp
from data_base import db


async def on_startup(_):
    print('bot is online')
    db.sql_start()


from handlers import client, admin, other

client.register_handlers_client(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
