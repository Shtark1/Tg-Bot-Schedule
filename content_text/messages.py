from telegram_bot.utils import StatesUsers

# СООБЩЕНИЯ ОТ БОТА
stat_message = """Привет 👋

Здесь ты можешь узнать своё расписание на сегодня или на всю недею"""
start_admin_message = """Приветствую админ 👋

Здесь ты можешь узнать своё расписание на сегодня или на всю недею"""
add_schedule_message = """Отправляй .xlsx файл с расписанием"""
not_xlsx_message = """Это не .xlsx файл"""
xlsx_message = """Расписание добавлено"""
not_command_message = """Такой команды нет"""
add_admin_message = """ID состоит только из чисел, его можно получить тут https://t.me/getmyid_bot
Вводи ID пользователя:"""
not_admin_id_message = """Это не число, ID состоит только из чисел, его можно получить тут https://t.me/getmyid_bot
Вводи ID пользователя:"""
del_tra_message = "Введи № для удаления расписания"
not_grp_message = "Такого номера нет!"
find_schedule_message = "Выберите кто вы"
which_group_message = "Введите номер вашей группы"
your_name_message = "Введите ваше ФИО в формате Иванов И.И."
what_day_message = "Выберите на какой день вам нужно расписание"
not_group_message = "Такого номера группы нет!"

MESSAGES = {
    "start": stat_message,
    "start_admin": start_admin_message,
    "add_schedule": add_schedule_message,
    "not_xlsx": not_xlsx_message,
    "xlsx": xlsx_message,
    "not_command": not_command_message,
    "add_admin": add_admin_message,
    "not_admin_id": not_admin_id_message,
    "del_tra": del_tra_message,
    "not_grp": not_grp_message,
    "find_schedule": find_schedule_message,
    "which_group": which_group_message,
    "your_name": your_name_message,
    "what_day": what_day_message,
    "not_group": not_group_message,
}
