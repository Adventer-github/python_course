# Чекушкин Д.А Вариант 22

# Ссылки на ER модель
# data/homework_var22.pdf
# data/homework_var22.png
# https://editor.ponyorm.com/user/test_student_test/homework_var22


import psycopg2
from random import randint
from create_tables import cmd_create_tables
import datetime


class ChildcareDatabase:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(
            database=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute(cmd_create_tables())

    def show_children_by_group(self, group_name):
        self.cursor.execute("""
            SELECT fio
            FROM children 
            WHERE groups = %s
        """, (group_name,))
        children = self.cursor.fetchall()
        return children

    def show_children_by_age(self, age):
        self.cursor.execute("""
            SELECT fio
            FROM children
            WHERE DATE_PART('year', age(date_trunc('year', CURRENT_DATE), birthdate)) = %s
        """, (age,))
        children = self.cursor.fetchall()
        return children

    def show_occupation_by_teacher(self, teacher_name):
        self.cursor.execute("""
            SELECT w.date, w.time, ws.work_name
            FROM walks w
            JOIN groups g ON w.groups = g.id
            JOIN wors_sheludes ws ON ws.groups = g.id
            JOIN group_employer ge ON ge.groupss = g.id
            JOIN employees e ON e.id = ge.employeess
            WHERE e.fio = %s
        """, (teacher_name,))
        occupations = self.cursor.fetchall()
        return occupations

    def show_occupation_by_group_and_day(self, group_name, day_of_week):
        self.cursor.execute("""
            SELECT w.time, ws.work_name
            FROM wors_sheludes ws
            JOIN walks w ON ws.groups = w.groups
            JOIN groups g ON w.groups = g.id
            WHERE g.group_name = %s AND ws.day = %s
        """, (group_name, day_of_week))
        occupations = self.cursor.fetchall()
        return occupations

    def show_gender_ratio_by_group(self, group_name):
        self.cursor.execute("""
            SELECT 
                COUNT(*) FILTER (WHERE c.sex = 'М') AS boys_count,
                COUNT(*) FILTER (WHERE c.sex = 'Ж') AS girls_count
            FROM children c
            JOIN groups g ON c.groups = g.id
            WHERE g.group_name = %s
        """, (group_name,))
        boys_count, girls_count = self.cursor.fetchone()
        total_count = boys_count + girls_count
        boys_percentage = (boys_count / total_count) * 100
        girls_percentage = (girls_count / total_count) * 100
        return boys_percentage, girls_percentage

    def find_group_name_by_child_name(self, child_name):
        self.cursor.execute("""
            SELECT g.group_name
            FROM children c
            JOIN groups g ON c.groups = g.id
            WHERE c.fio = %s
        """, (child_name,))
        group_name = self.cursor.fetchone()
        return group_name

    def add_child_to_table(self, fio, birthdate, sex, group_id):
        today = datetime.date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        if age < 2 or age > 7:
            raise ValueError("Invalid age. Child's age should be between 2 and 7 years.")

        self.cursor.execute("""
            INSERT INTO children ("fio", "birthdate", "sex", "groups") VALUES (%s, %s, %s, %s)
        """, (fio, birthdate, sex, group_id))

    def fill_database_with_random_data(self):
        group_names = ['Group A', 'Group B', 'Group C']
        teacher_names = ['John Smith', 'Emma Johnson', 'Michael Davis']
        child_names = ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace']
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        work_names = ['Music', 'Sports', 'Art']

        for teacher_name in teacher_names:
            self.cursor.execute("""
                INSERT INTO employees ("fio", "title") VALUES (%s, 'Teacher')
            """, (teacher_name,))

        for group_name in group_names:
            self.cursor.execute("""
                INSERT INTO groups ("group_name", "count_of_children") VALUES (%s, %s)
            """, (group_name, randint(10, 20)))

        for child_name in child_names:
            birthdate = "2019-01-01"
            sex = 'М' if randint(0, 1) == 0 else 'Ж'
            group_id = randint(1, len(group_names))

            self.cursor.execute("""
                INSERT INTO children ("fio", "birthdate", "sex", "groups") VALUES (%s, %s, %s, %s)
            """, (child_name, birthdate, sex, group_id))

        for group_id in range(1, len(group_names) + 1):
            teacher_id = randint(1, len(teacher_names))
            self.cursor.execute("""
                INSERT INTO group_employer ("groupss", "employeess") VALUES (%s, %s)
            """, (group_id, teacher_id))

        for _ in range(10):
            date = "2023-01-01"
            time = "Morning" if randint(0, 1) == 0 else "Afternoon"
            group_id = randint(1, len(group_names))

            self.cursor.execute("""
                INSERT INTO walks ("date", "time", "groups") VALUES (%s, %s, %s)
            """, (date, time, group_id))

        for group_id in range(1, len(group_names) + 1):
            day_of_week = days_of_week[randint(0, len(days_of_week) - 1)]
            room = randint(100, 200)
            work_name = work_names[randint(0, len(work_names) - 1)]

            self.cursor.execute("""
                INSERT INTO wors_sheludes ("day", "room", "groups", "work_name") VALUES (%s, %s, %s, %s)
            """, (day_of_week, room, group_id, work_name))

        self.conn.commit()


postgres = ChildcareDatabase("homework", "homework", "homework", "localhost", "5432")
postgres.create_tables()
postgres.fill_database_with_random_data()
print(postgres.show_children_by_group("1"))
print(postgres.show_children_by_age("4"))
print(postgres.show_occupation_by_teacher(teacher_name="Emma Johnson"))
print(postgres.show_occupation_by_group_and_day("Group B", "Friday"))
print(postgres.show_gender_ratio_by_group("Group A"))
print(postgres.find_group_name_by_child_name("David"))

# Добавление ребенка в садик
fio = "John Doe"
birthdate = datetime.date(2018, 5, 10)
sex = "М"
group_id = 1

try:
    postgres.add_child_to_table(fio, birthdate, sex, group_id)
    print("Child added successfully!")
except ValueError as e:
    print("Error:", str(e))
