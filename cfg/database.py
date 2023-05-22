import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_training(self, day_of_the_week, num, auditorium, view, teacher, discipline, group, parity):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `training` (`day of the week`, `num`, `auditorium`, `view`, `teacher`, `discipline`, `group`, `parity`) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (day_of_the_week, num, auditorium, view, teacher, discipline, group, parity,))

    def ins_group(self):
        with self.connection:
            self.cursor.execute("SELECT DISTINCT `group` FROM `training`")
            unique_groups = self.cursor.fetchall()
            return [group[0] for group in unique_groups]

    def del_group(self, group):
        with self.connection:
            return self.cursor.execute("DELETE FROM `training` WHERE `group` = ?", (group,))

    def check_group(self, group):
        with self.connection:
            self.cursor.execute("SELECT COUNT(*) FROM `training` WHERE `group` = ?", (group,))
            result = self.cursor.fetchone()[0]
            return result > 0

    def check_teacher(self, teacher):
        with self.connection:
            self.cursor.execute("SELECT COUNT(*) FROM `training` WHERE `teacher` = ?", (teacher,))
            result = self.cursor.fetchone()[0]
            return result > 0

    def get_training(self, column1_name, column2_name, column1_value, column2_value):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM `training` WHERE `{column1_name}` = ? AND `{column2_name}` = ?",
                                       (column1_value, column2_value)).fetchall()
