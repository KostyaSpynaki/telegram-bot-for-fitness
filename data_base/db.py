import sqlite3 as sq


def sql_start():
    global base, curs
    base = sq.connect('data_base.sqlite3')
    curs = base.cursor()
    if base:
        print('connect to base')


async def add_user(state):
    async with state.proxy() as data:
        curs.execute('INSERT INTO users VALUES (?, ?, ?)', tuple(data.values()))
        base.commit()


async def find_user(user_id):
    user = curs.execute('SELECT * FROM users WHERE id={}'.format(user_id)).fetchone()
    if user is not None:
        return True
