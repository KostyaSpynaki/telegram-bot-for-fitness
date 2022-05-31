import sqlite3 as sq


# установка соединения с бд
def sql_start():
    global base, curs
    base = sq.connect('data_base.sqlite3')
    curs = base.cursor()
    if base:
        print('connect to base')


# добовляет пользователя в бд
async def add_user(state):
    async with state.proxy() as data:
        curs.execute('INSERT INTO users VALUES (?, ?, ?)', tuple(data.values()))
        base.commit()


# сохроняеи прогресс пользователя
async def save_users_exercises(state):
    async with state.proxy() as data:
        curs.execute('INSERT INTO user_progress VALUES (?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()


# проверят наличие пользователя в бд
async def find_user(user_id):
    user = curs.execute('SELECT * FROM users WHERE id={}'.format(user_id)).fetchone()
    if user is not None:
        return True


# получает все категории
async def get_categories():
    categories = curs.execute('SELECT * FROM categorys').fetchall()
    return categories


# получает все упражения заданной категории
async def get_sub_categories(cat_id):
    sub_categories = curs.execute('SELECT * FROM exercises WHERE cat_id = ?', (cat_id,))
    return sub_categories


# async def select_progress(cat, us_id):
#     progress = curs.execute('select weight, repeats, exercises.name  from user_progress join exercises on exerc_id == exercises.id join categorys on exercises.cat_id == categorys.cat_id where categorys.name == "{}" and user_progress.use_id == {}'.format(cat, us_id)).fetchall()
#     return progress

# получает прогресс конкретного пользователя
async def get_progress(exercises_id, user_id):
    print(user_id)
    progress = curs.execute(
        'select weight, repeats, date from user_progress where exerc_id = ? and user_progress.use_id = ?',
        (exercises_id, user_id)).fetchall()
    return progress


# получает последнюю запись пользователя
async def get_progress_user_last(exercises_id, user_id):
    progress = curs.execute(
        'select weight, repeats, max(date) from user_progress where exerc_id = ? and user_progress.use_id = ?',
        (exercises_id, user_id)).fetchone()
    return progress


# получает записи за последний месяц
async def get_progress_user_month(exercises_id, user_id):
    progress = curs.execute(
        'select weight, repeats, date from user_progress where exerc_id = ? and user_progress.use_id = ? and '
        'date > (select max(date) from user_progress where exerc_id = ? and use_id = ? ) - 2629743',
        (exercises_id, user_id, exercises_id, user_id)).fetchall()
    print(progress)
    return progress
