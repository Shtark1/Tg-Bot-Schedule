# ШАБЛОН ОТПРАВКИ РАСПИСАНИЯ ДЛЯ СТУДЕНТОВ
async def send_student(db, day_name, student, callback):
    if day_name.lower() != "воскресенье":
        all_traning = db.get_training("day of the week", "group", f"{day_name.lower()}", student)
        await callback.message.answer(fr"""<b>Расписание на {day_name}</b>

<b>НЕЧЁТНАЯ НЕДЕЛЯ</b>   

            <b>Ауд.    Предмет    Препод.    Вид.</b>    

<b>1.</b> <u>{all_traning[0][3]}  {all_traning[0][6]}  {all_traning[0][5]}  {all_traning[0][4]}</u>
<b>2.</b> <u>{all_traning[2][3]}  {all_traning[2][6]}  {all_traning[2][5]}  {all_traning[2][4]}</u>
<b>3.</b> <u>{all_traning[4][3]}  {all_traning[4][6]}  {all_traning[4][5]}  {all_traning[4][4]}</u> 
<b>4.</b> <u>{all_traning[6][3]}  {all_traning[6][6]}  {all_traning[6][5]}  {all_traning[6][4]}</u>
<b>5.</b> <u>{all_traning[8][3]}  {all_traning[8][6]}  {all_traning[8][5]}  {all_traning[8][4]}</u>

<b>ЧЁТНАЯ НЕДЕЛЯ</b>   

            <b>Ауд.    Предмет    Препод.    Вид.</b>    

<b>1.</b> <u>{all_traning[1][3]}  {all_traning[1][6]}  {all_traning[1][5]}  {all_traning[1][4]}</u>
<b>2.</b> <u>{all_traning[3][3]}  {all_traning[3][6]}  {all_traning[3][5]}  {all_traning[3][4]}</u>
<b>3.</b> <u>{all_traning[5][3]}  {all_traning[5][6]}  {all_traning[5][5]}  {all_traning[5][4]}</u> 
<b>4.</b> <u>{all_traning[7][3]}  {all_traning[7][6]}  {all_traning[7][5]}  {all_traning[7][4]}</u>
<b>5.</b> <u>{all_traning[9][3]}  {all_traning[9][6]}  {all_traning[9][5]}  {all_traning[9][4]}</u>
    """, parse_mode='HTML')


# ШАБЛОН ОТПРАВКИ РАСПИСАНИЯ ДЛЯ ПРЕПОДАВАТЕЛЕЙ
async def send_teacher(db, day_name, teacher, callback):
    if day_name.lower() != "воскресенье":
        all_traning = db.get_training("day of the week", "teacher", f"{day_name.lower()}", teacher)

        text = fr"""<b>Расписание на {day_name}</b>

<b>НЕЧЁТНАЯ НЕДЕЛЯ</b>   

                <b>Ауд.    Предмет    Препод.    Вид.    Группа.</b>   
    """

        i = 0
        while i < len(all_traning):
            if all_traning[i][8] == "нечетная неделя":
                text2 = fr"""
<b>{all_traning[i][2]}</b> <u>{all_traning[i][3]}  {all_traning[i][6]}  {all_traning[i][5]}  {all_traning[i][4]}  {all_traning[i][7]}</u>"""
            text += text2
            i += 1
        text += """

<b>ЧЁТНАЯ НЕДЕЛЯ</b>   

                <b>Ауд.    Предмет    Препод.    Вид.    Группа.</b>   
    """
        i = 0
        while i < len(all_traning):
            if all_traning[i][8] == "четная неделя":
                text2 = fr"""
<b>{all_traning[i][2]}</b> <u>{all_traning[i][3]}  {all_traning[i][6]}  {all_traning[i][5]}  {all_traning[i][4]}  {all_traning[i][7]}</u>"""
                text += text2
            i += 1

        await callback.message.answer(text, parse_mode='HTML')
