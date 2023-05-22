import datetime
import locale
import calendar
import logging

from aiogram import Bot
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from telegram_bot.utils import StatesUsers, StatesAdmin
from telegram_bot.KeyboardButton import BUTTON_TYPES
from content_text.messages import MESSAGES
from cfg.cfg import TOKEN, ADMIN_ID
from cfg.database import Database
from dop_functional.add_db import read_excel
from dop_functional.send_training import send_student, send_teacher


db = Database('cfg/database')

logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

dp.middleware.setup(LoggingMiddleware())


# ===================================================
# ===================== АДМИНКА =====================
# ===================================================
@dp.message_handler(lambda message: message.text.lower() == 'добавить расписание')
async def start_command(message: Message):
    if message.from_user.id in ADMIN_ID:
        await message.answer(MESSAGES["add_schedule"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])

        state = dp.current_state(user=message.from_user.id)
        await state.set_state(StatesAdmin.all()[0])

    else:
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME"])


# =============== ПОЛУЧЕНИЕ .xlsx ФАЙЛА ===============
@dp.message_handler(state=StatesAdmin.STATES_0)
async def start_command(message: Message, state: FSMContext):
    await state.finish()
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
    else:
        await message.answer(MESSAGES['not_xlsx'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])


@dp.message_handler(content_types=ContentType.DOCUMENT, state=StatesAdmin.STATES_0)
async def scan_message(message: Message, state: FSMContext):
    await state.finish()
    if message.document.file_name[-5:] == ".xlsx":
        cd = fr"{message.document.file_name}"
        await message.document.download(cd)
        read_excel(db, cd)
        await message.answer(MESSAGES['xlsx'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
    else:
        await message.answer(MESSAGES['not_xlsx'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])


# =============== УДАЛИТЬ РАСПИСАНИЕ ===============
@dp.message_handler(lambda message: message.text.lower() == 'удалить расписание')
async def start_command(message: Message):
    if message.from_user.id in ADMIN_ID:
        all_groups = db.ins_group()
        await message.answer(MESSAGES['del_tra'], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        for idx, grp in enumerate(all_groups):
            await message.answer(f"{idx+1}. {grp}")

        state = dp.current_state(user=message.from_user.id)
        await state.set_state(StatesAdmin.all()[2])

    else:
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME"])


# =============== ВВОД № ДЛЯ УДАЛЕНИЯ ГРУППЫ ===============
@dp.message_handler(state=StatesAdmin.STATES_2)
async def start_command(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()

    elif message.text.isnumeric():
        all_groups = db.ins_group()
        for idx, grp in enumerate(all_groups):
            if idx+1 == int(message.text):
                db.del_group(grp)

        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()

    else:
        await message.answer(MESSAGES["not_grp"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesAdmin.all()[1])


# =============== ДОБАВИТЬ АДМИНА ===============
@dp.message_handler(lambda message: message.text.lower() == 'добавить админа')
async def start_command(message: Message):
    if message.from_user.id in ADMIN_ID:
        await message.answer(MESSAGES["add_admin"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(StatesAdmin.all()[1])

    else:
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME"])


# =============== ВВОД ID АДМИНА ===============
@dp.message_handler(state=StatesAdmin.STATES_1)
async def start_command(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    elif message.text.isnumeric():
        new_users_id = int(message.text)
        ADMIN_ID.append(new_users_id)
        await message.answer("Добавил!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        await message.answer(MESSAGES["not_admin_id"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesAdmin.all()[1])


# =============== ОТМЕНА ===============
@dp.message_handler(lambda message: message.text.lower() == 'отмена')
async def start_command(message: Message):
    if message.from_user.id in ADMIN_ID:
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])


# ===================================================
# =============== СТАНДАРТНЫЕ КОМАНДЫ ===============
# ===================================================
@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    if message.from_user.id in ADMIN_ID:
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])

    else:
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME"])


# =============== УЗНАТЬ РАСПИСАНИЕ ===============
@dp.message_handler(lambda message: message.text.lower() == 'узнать расписание')
async def start_command(message: Message):
    await message.answer(MESSAGES['find_schedule'], reply_markup=BUTTON_TYPES["BTN_WHO_IN"])


# =============== ЗАПРОС ГРУППЫ ИЛИ ФАМИЛИИ ===============
@dp.callback_query_handler(lambda c: c.data == "student" or c.data == "teacher")
async def start_command(callback: CallbackQuery):
    state = dp.current_state(user=callback.from_user.id)

    if callback.data == "student":
        await callback.message.edit_text(MESSAGES["which_group"])
        await state.set_state(StatesUsers.all()[0])

    elif callback.data == "teacher":
        await callback.message.edit_text(MESSAGES["your_name"])
        await state.set_state(StatesUsers.all()[0])

    await callback.message.edit_reply_markup(BUTTON_TYPES["BTN_CANCEL_IN"])


# =============== ВВОД ГРУППЫ ИЛИ ФИО ===============
@dp.message_handler(state=StatesUsers.STATE_0)
async def start_command(message: Message, state: FSMContext):
    if db.check_group(message.text):
        await state.update_data(group=message.text)
        await state.update_data(name=False)
        await message.answer(MESSAGES["what_day"], reply_markup=BUTTON_TYPES["BTN_WHAT_DAY"])
        await state.set_state(StatesUsers.all()[1])

    elif db.check_teacher(message.text):
        await state.update_data(group=False)
        await state.update_data(name=message.text)
        await message.answer(MESSAGES["what_day"], reply_markup=BUTTON_TYPES["BTN_WHAT_DAY"])
        await state.set_state(StatesUsers.all()[1])

    else:
        await message.answer(MESSAGES['not_group'])
        if message.from_user.id in ADMIN_ID:
            await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        else:
            await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME"])
        await state.finish()


# =============== НА КАКОЙ ДЕНЬ РАСПИСАНИЕ ===============
@dp.callback_query_handler(state=StatesUsers.STATE_1)
async def start_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    locale.setlocale(locale.LC_ALL, 'ru_RU')
    today = datetime.date.today()

    data = await state.get_data()
    student = data["group"]
    teacher = data["name"]

    if callback.data == "today":
        day_number = today.weekday()
        day_name = calendar.day_name[day_number]

        if student:
            await callback.message.delete()
            await send_student(db, day_name, student, callback)

        else:
            await send_teacher(db, day_name, teacher, callback)

    elif callback.data == "three_day":
        tomorrow = today + datetime.timedelta(days=1)
        day_after_tomorrow = today + datetime.timedelta(days=2)
        days = [today, tomorrow, day_after_tomorrow]
        day_names = [calendar.day_name[day.weekday()] for day in days]

        if student:
            await send_student(db, day_names[0], student, callback)
            await send_student(db, day_names[1], student, callback)
            await send_student(db, day_names[2], student, callback)

        else:
            await send_teacher(db, day_names[0], teacher, callback)
            await send_teacher(db, day_names[1], teacher, callback)
            await send_teacher(db, day_names[2], teacher, callback)

    elif callback.data == "all_day":
        if student:
            await send_student(db, "понедельник", student, callback)
            await send_student(db, "вторник", student, callback)
            await send_student(db, "среда", student, callback)
            await send_student(db, "четверг", student, callback)
            await send_student(db, "пятница", student, callback)
            await send_student(db, "суббота", student, callback)
        else:
            await send_teacher(db, "понедельник", teacher, callback)
            await send_teacher(db, "вторник", teacher, callback)
            await send_teacher(db, "среда", teacher, callback)
            await send_teacher(db, "четверг", teacher, callback)
            await send_teacher(db, "пятница", teacher, callback)
            await send_teacher(db, "суббота", teacher, callback)

    await state.finish()


# =============== ОТМЕНА ИНЛАЙН ===============
@dp.callback_query_handler(state=StatesUsers.STATE_0)
@dp.callback_query_handler(state=StatesUsers.STATE_1)
@dp.callback_query_handler(lambda c: c.data == "cancel")
async def start_command(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    if callback.from_user.id in ADMIN_ID:
        await callback.message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
    else:
        await callback.message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME"])


# =============== НЕИЗВЕСТНАЯ КОМАНДА ===============
@dp.message_handler()
async def start_command(message: Message):
    if message.from_user.id in ADMIN_ID:
        await message.answer(MESSAGES['not_command'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
    else:
        await bot.send_message(message.from_user.id, MESSAGES["not_command"], reply_markup=BUTTON_TYPES["BTN_HOME"])


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


def start():
    executor.start_polling(dp, on_shutdown=shutdown)
