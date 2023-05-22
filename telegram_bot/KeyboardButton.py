from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

# КНОПКИ МЕНЮ
btn_home = KeyboardButton("Узнать расписание")
btn_home_admin = KeyboardButton("Добавить расписание")
btn_home_admin_del = KeyboardButton("Удалить расписание")
btn_cancel = KeyboardButton("Отмена")
btn_add_admin = KeyboardButton("Добавить админа")

# УЗНАТЬ РАСПИСАНИЕ
btn_student = KeyboardButton("Я студент")
btn_teacher = KeyboardButton("Я преподаватель")

# УЗНАТЬ РАСПИСАНИЕ
btn_student_in = InlineKeyboardButton(text="Я студент", callback_data="student")
btn_teacher_in = InlineKeyboardButton(text="Я преподаватель", callback_data="teacher")
btn_cancel_in = InlineKeyboardButton(text="Отмена", callback_data="cancel")

# НА КАКОЙ ДЕНЬ
btn_today = InlineKeyboardButton(text="На сегодня", callback_data="today")
btn_three_day = InlineKeyboardButton(text="На три дня", callback_data="three_day")
btn_all_day = InlineKeyboardButton(text="На неделю", callback_data="all_day")


# ОПАТА
# btn_check_pay = InlineKeyboardButton(text="Проверить ещё раз", callback_data="AGAIN")
# btn_pay_cancel = InlineKeyboardButton(text="Отмена", callback_data="CANCEL")


BUTTON_TYPES = {
    "BTN_HOME": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_home),
    "BTN_HOME_ADMIN": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_home_admin, btn_home_admin_del).add(btn_add_admin).add(btn_home),
    "BTN_CANCEL": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_cancel),
    "BTN_WHO": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_student).add(btn_teacher),
    "BTN_WHO_IN": InlineKeyboardMarkup().add(btn_student_in, btn_teacher_in).add(btn_cancel_in),
    "BTN_CANCEL_IN": InlineKeyboardMarkup().add(btn_cancel_in),
    "BTN_WHAT_DAY": InlineKeyboardMarkup().add(btn_today, btn_three_day, btn_all_day).add(btn_cancel_in),

    "BTN_CANCE": InlineKeyboardMarkup().add(),
}
