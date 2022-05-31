import datetime


# функция переволить данные из бд в нормальный вид
def parse(progress_list):
    if progress_list and progress_list[0] is not None:
        if type(progress_list) == list:
            format_string = [f'Кол-во повторов: {pr[1]} \nВес: {pr[0]} kg\nДата: {date_format(pr[2])} \n' for pr in
                             progress_list]
            return ''.join(format_string)
        elif type(progress_list) == tuple:
            format_string = f'Кол-во повторов: {progress_list[1]} \nВес: {progress_list[0]} kg\nДата: {date_format(progress_list[2])} \n'
            return format_string
    else:
        return 'У вас пока нет записей'


def date_format(date):
    if not date:
        return ''
    date_now = datetime.datetime.fromtimestamp(float(date)).strftime('%d-%m-%Y')
    return date_now
