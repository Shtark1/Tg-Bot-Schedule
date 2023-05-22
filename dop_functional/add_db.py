import os
from openpyxl import load_workbook


def read_excel(db, cd):
    day_of_the_week = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота"]
    row_in = ["3:7", "8:12", "13:17", "18:22", "23:27", "28:32"]
    wb = load_workbook(cd)['Лист1']

    group = wb["A33"].value

    for ind, week in enumerate(day_of_the_week):
        column = wb[row_in[ind]]
        for column in column:
            all_date = [column[x].value for x in range(len(column))]

            if all_date[8] is None and all_date[3] is None:
                db.add_training(week, "-", "-", "-", "-", "-", group, "нечетная неделя")
                db.add_training(week, "-", "-", "-", "-", "-", group, "нечетная неделя")

            elif all_date[3] is None:
                db.add_training(week, "-", "-", "-", "-", "-", group, "нечетная неделя")
                db.add_training(week, all_date[1], all_date[10], all_date[9], all_date[8], all_date[7], group, "четная неделя")

            elif all_date[8] is None:
                db.add_training(week, all_date[1], all_date[3], all_date[4], all_date[5], all_date[6], group, "нечетная неделя")
                db.add_training(week, "-", "-", "-", "-", "-", group, "нечетная неделя")

            else:
                db.add_training(week, all_date[1], all_date[3], all_date[4], all_date[5], all_date[6], group, "нечетная неделя")
                db.add_training(week, all_date[1], all_date[10], all_date[9], all_date[8], all_date[7], group, "четная неделя")

    os.remove(cd)
