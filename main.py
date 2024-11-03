import sqlite3
conn = sqlite3.connect('university.db')
cursor = conn.cursor()

cursor.execute(''' PRAGMA foreign_keys = ON ''')

from datetime import  datetime

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        print("Неправильный формат даты. Используйте YYYY-MM-DD.")
        return False



class Students:
    def create(self):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Students (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Surname TEXT NOT NULL,
                Fak TEXT NOT NULL,
                DateOfBirth DATE NOT NULL
            )''')
        conn.commit()
    def add(self, name, surname, department, date_of_birth): #1
        cursor.execute('''
            INSERT INTO Students (Name, Surname, Fak, DateOfBirth)
            VALUES (?, ?, ?, ?)''', (name, surname, department, date_of_birth))
        conn.commit()
    def update(self, student_id, name, surname, department, date_of_birth): #2
        cursor.execute('''
            UPDATE Students
            SET Name = ?, Surname = ?, Fak = ?, DateOfBirth = ?
            WHERE ID = ?''', (name, surname, department, date_of_birth, student_id))
        conn.commit()
    def delete(self, student_id): #3
        cursor.execute('DELETE FROM Students WHERE ID = ?', (student_id,))
        conn.commit()
    def delete_students(self):
        cursor.execute("DROP TABLE Students")
        conn.commit()
    def get_by_fak(self, department): #4
        cursor.execute('SELECT Name, Surname, DateOfBirth FROM Students WHERE Fak = ?', (department,))
        students = cursor.fetchall()
        return students
    def get_by_course(self, course_id): #6
        cursor.execute("""
            SELECT Students.ID, Name, Surname, DateOfBirth
            FROM Students
            INNER JOIN Grades ON Grades.StudentID = Students.ID
            INNER JOIN Exams ON Exams.ID = Grades.ExamID
            INNER JOIN Courses ON Courses.ID = Exams.CourseID
            WHERE Courses.ID = ?""", (course_id))
        students = cursor.fetchall()
        return students

class Teachers:
    def create(self):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Teachers (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Surname TEXT NOT NULL,
                Kaf TEXT NOT NULL
            )''')
    def add(self, name, surname, department):
        cursor.execute('''
                    INSERT INTO Teachers (Name, Surname, Kaf)
                    VALUES (?, ?, ?)''', (name, surname, department))
        conn.commit()
    def update(self, name, surname, department, teacher_id):
        cursor.execute('''
                    UPDATE Teachers
                    SET Name = ?, Surname = ?, kaf = ?
                    WHERE ID = ?''', (name, surname, department, teacher_id))
        conn.commit()
    def delete(self, teacher_td):
        cursor.execute('DELETE FROM Teachers WHERE ID = ?', (teacher_td,))
        conn.commit()
    def delete_teachers(self):
        cursor.execute("DROP TABLE Teachers")
        conn.commit()

class Courses:
    def create(self):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Courses (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Title TEXT NOT NULL,
                Description TEXT,
                TeacherID INTEGER,
                FOREIGN KEY (TeacherID) REFERENCES Teachers(ID) ON DELETE CASCADE
            )''')
    def add(self, title, description, teacherID):
        cursor.execute('''
            INSERT INTO Courses (Title, Description, TeacherID)
            VALUES (?, ?, ?)''', (title, description, teacherID))
        conn.commit()
    def update(self, title, description, teacher_id, course_id): #2
        cursor.execute('''
            UPDATE Courses
            SET Title = ?, Description = ?, TeacherID = ?
            WHERE ID = ?''', (title, description, teacher_id, course_id))
        conn.commit()
    def delete(self, course_id):
        cursor.execute('DELETE FROM Courses WHERE ID = ?', (course_id,))
        conn.commit()
    def delete_courses(self):
        cursor.execute("DROP TABLE Courses")
    def get_by_teacher(self, teacher_id): #5
        cursor.execute('SELECT * FROM Courses WHERE TeacherID = ?', (teacher_id,))
        courses = cursor.fetchall()
        return courses

class Exams:
    def create(self):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Exams (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Date DATE NOT NULL,
                MaxScore INTEGER,
                CourseID INTEGER,
                FOREIGN KEY (CourseID) REFERENCES Courses(ID) ON DELETE CASCADE 
            )''')
    def add(self, date, max_score, course_id):
        cursor.execute('''
            INSERT INTO Exams (Date, MaxScore, CourseID)
            VALUES (?, ?, ?)''', (date, max_score, course_id))
        conn.commit()
    def update(self, date, maxscore, courseid, exam_id):
        cursor.execute('''
            UPDATE Exams
            SET Date = ?, MaxScore = ?, CourseID = ?
            WHERE ID = ?''', (date, maxscore, courseid, exam_id))
        conn.commit()
    def delete(self, exam_id):
        cursor.execute('DELETE FROM Exams WHERE ID = ?', (exam_id,))
        conn.commit()
    def delete_exams(self):
        cursor.execute("DROP TABLE Exams")

class Grades:
    def create(self):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Grades (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Score INTEGER,
            StudentID INTEGER,
            ExamID INTEGER,
            FOREIGN KEY (StudentID) REFERENCES Students(ID) ON DELETE CASCADE,
            FOREIGN KEY (ExamID) REFERENCES Exams(ID) ON DELETE CASCADE
        )''')
    def add(self, score, student_id, exam_id):
        cursor.execute('''
            INSERT INTO Grades (Score, StudentID, ExamID)
            VALUES (?, ?, ?)''', (score, student_id, exam_id))
        conn.commit()
    def update(self, score, student_id, exam_id, grade_id):
        cursor.execute('''
            UPDATE Grades
            SET Score = ?, StudentID = ?, ExamID = ?
            WHERE ID = ?''', (score, student_id, exam_id, grade_id))
        conn.commit()
    def delete(self, grade_id):
        cursor.execute('DELETE FROM Grades WHERE ID = ?', (grade_id,))
        conn.commit()
    def delete_grades(self):
        cursor.execute("DROP TABLE Grades")
    def get_by_student_course(self, course_id): #19
        cursor.execute("""
            SELECT StudentID, Score
            FROM Grades
            INNER JOIN Exams ON Exams.ID = Grades.ExamID
            INNER JOIN Courses ON Courses.ID = Exams.CourseID
            WHERE Courses.ID = ?""", (course_id,))
        grades = cursor.fetchall()
        return grades
    def get_avg_by_course_student(self, student_id, course_id): #20
        cursor.execute("""
            SELECT AVG(Score)
            FROM Grades
            INNER JOIN Exams ON Exams.ID = Grades.ExamID
            INNER JOIN Courses ON Courses.ID = Exams.CourseID
            WHERE Courses.ID = ? AND Grades.StudentID = ? """, (course_id, student_id,))
        avg_grades = cursor.fetchall()
        return avg_grades
    def get_avg_by_student(self, student_id): #21
        cursor.execute("""
            SELECT AVG(Score)
            FROM Grades
            WHERE Grades.StudentID = ? """, (student_id,))
        avg_grades = cursor.fetchall()
        return avg_grades
    def get_avg_by_fak(self, fak_name): #22
        cursor.execute("""
            SELECT AVG(Score)
            FROM Grades
            INNER JOIN Students ON Students.ID = Grades.StudentID
            WHERE Students.Fak = ?""", (fak_name,))
        avg_grades = cursor.fetchall()
        return avg_grades


def create_database(s, t, c, e, g):
    s.create()
    t.create()
    c.create()
    e.create()
    g.create()
def delete_all(s, t, c, e, g):
    s.delete_students()
    s.create()
    t.delete_teachers()
    t.create()
    c.delete_courses()
    c.create()
    e.delete_exams()
    e.create()
    g.delete_grades()
    g.create()

def main():
    s = Students()
    t = Teachers()
    c = Courses()
    e = Exams()
    g = Grades()
    create_database(s, t, c, e, g)
    while True:
        print("\nВыберите действие:")
        print("1. Добавить студента")
        print("2. Изменить студента")
        print("3. Удалить студента")
        print("4. Получить список студентов по факультету")
        print("5. Получить список студентов, зачисленных на конкретный курс")
        print("6. Добавить преподавателя")
        print("7. Изменить преподавателя")
        print("8. Удалить преподавателя")
        print("9. Добавить курс")
        print("10. Изменить курс")
        print("11. Удалить курс")
        print("12. Получить список курсов, читаемых преподавателем")
        print("13. Добавить экзамен")
        print("14. Изменить экзамен")
        print("15. Удалить экзамен")
        print("16. Добавить оценку")
        print("17. Изменить оценку")
        print("18. Удалить оценку")
        print("19. Получить оценки студентов по определенному курсу")
        print("20. Получить средний бал студента по определенному курсу")
        print("21. Получить средний бал студента в целом")
        print("22. Получить средний был по факультету")
        print("23. Удаление данных")
        print("24. Выйти")

        choice = input("Введите номер действия: ")

        if choice == '1':
            try:
                name = input("Имя студента: ")
                surname = input("Фамилия студента: ")
                department = input("Факультет студента: ")
                date_of_birth = input("Дата рождения студента (YYYY-MM-DD): ")
                if validate_date(date_of_birth):
                    s.add(name, surname, department, date_of_birth)
                    print("Студент добавлен")
                else:
                    print("Ошибка при вводе даты")
            except Exception as e:
                print("Ошибка при добавлении студента \n", e)
        elif choice == '2':
            try:
                student_id = int(input("ID студента: "))
                name = input("Новое имя студента: ")
                surname = input("Новая фамилия студента: ")
                department = input("Новое отделение студента: ")
                date_of_birth = input("Новая дата рождения студента (YYYY-MM-DD): ")
                if validate_date(date_of_birth):
                    s.update(student_id, name, surname, department, date_of_birth)
                    print("Информация о студенте изменена")
                else:
                    print("Ошибка при вводе даты")
            except Exception as e:
                print("Ошибка при изменении информации о студента \n", e)
        elif choice == '3':
            try:
                student_id = int(input("ID студента: "))
                s.delete(student_id)
                print("Студент удален")
            except Exception as e:
                print("Ошибка при удалении стулента \n", e)
        elif choice == '4':
            try:
                department = input("Факультет: ")
                students = s.get_by_fak(department)
                for student in students:
                    print(student)
            except Exception as e:
                    print("Ошибка при получении студентов на факультете \n", e)
        elif choice == '5':
            try:
                department = input("Номер курса: ")
                students = s.get_by_course(department)
                print(students)
            except Exception as e:
                print("Ошибка при получении студентов на курсе \n", e)
        elif choice == '6':
            try:
                name = input("Имя преподавателя: ")
                surname = input("Фамилия преподавателя: ")
                department = input("Кафедра преподавателя: ")
                t.add(name, surname, department)
                print("Преподаватель добавлен")
            except Exception as e:
                print("Ошибка при добавлении преподавателя \n", e)
        elif choice == '7':
            try:
                teacher_id = int(input("ID преподавателя: "))
                name = input("Новое имя преподавателя: ")
                surname = input("Новая фамилия преподавателя: ")
                department = input("Новая кафедра преподавателя: ")
                t.update(name, surname, department, teacher_id)
                print("Информация о преподавателе изменена")
            except Exception as e:
                print("Ошибка при изменении информации о преподавателе \n", e)
        elif choice == '8':
            try:
                teacher_id = int(input("ID преподавателя: "))
                t.delete(teacher_id)
                print("Преподаватель удален")
            except Exception as e:
                print("Ошибка при удалении преподавателя \n", e)
        elif choice == '9':
            try:
                title = input("Название курса: ")
                description = input("Описание курса: ")
                teacher_id = int(input("ID преподавателя: "))
                c.add(title, description, teacher_id)
                print("Курс добавлен")
            except Exception as e:
                print("Ошибка при добавлении курса \n", e)
        elif choice == '10':
            try:
                course_id = int(input("ID курса"))
                title = input("Новое название курса: ")
                description = input("Новое описание курса: ")
                teacher_id = int(input("Новое ID преподавателя: "))
                c.update(title, description, teacher_id, course_id)
                print("Информация о курсе изменена")
            except Exception as e:
                print("Ошибка при изменении курса \n", e)
        elif choice == '11':
            try:
                course_id = int(input("Номер курса: "))
                c.delete(course_id)
                print("Курс удален")
            except Exception as e:
                print("Ошибка при удалении курса \n", e)
        elif choice == '12':
            try:
                teacher_id = int(input("ID преподавателя: "))
                courses = c.get_by_teacher(teacher_id)
                for course in courses:
                    print(course)
            except Exception as e:
                print("Ошибка при получении списка курсов по преподавателю \n", e)
        elif choice == '13':
            try:
                date = input("Дата экзамена (YYYY-MM-DD): ")
                if validate_date(date):
                    course_id = int(input("ID курса: "))
                    max_score = int(input("Максимальный балл: "))
                    e.add(date, max_score, course_id)
                    print("Экзамен добавлен")
                else:
                    print("Ошибка при вводе даты")
            except Exception as x:
                print("Ошибка при добавлении экзамена \n", x)
        elif choice == '14':
            try:
                exam_id = int(input("ID экзамена: "))
                date = input("Новая дата экзамена (YYYY-MM-DD): ")
                if validate_date(date):
                    course_id = int(input("Новое ID курса: "))
                    max_score = int(input("Новый максимальный балл: "))
                    e.update(date, max_score, course_id, exam_id)
                    print("Информация об экзамене изменена")
                else:
                    print("Ошибка при вводе даты")
            except Exception as q:
                print("Ошибка при изменении информации об экзамене \n", q)
        elif choice == '15':
            try:
                exam_id = int(input("ID экзамена: "))
                e.delete(exam_id)
                print("Экзамен удален")
            except Exception as q:
                print("Ошибка при удалении экзаменов \n", q)
        elif choice == '16':
            try:
                score = int(input("Результат: "))
                student_id = int(input("ID студента: "))
                exam_id = int(input("ID экзамена: "))
                g.add(score, student_id, exam_id)
                print("Оценка добавлена")
            except Exception as e:
                print("Ошибка при добавлении оценки \n", e)
        elif choice == '17':
            try:
                grade_id = int(input("ID оценки"))
                score = int(input("Новый результат: "))
                student_id = int(input("Новый ID студента: "))
                exam_id = int(input("Новый ID экзамена: "))
                g.update(score, student_id, exam_id, grade_id)
                print("Оценка изменена")
            except Exception as e:
                print("Ошибка при изменении оценки \n", e)
        elif choice == '18':
            try:
                grade_id = int(input("ID оценки: "))
                g.delete(grade_id)
                print("Оценка удалена")
            except Exception as e:
                print("Ошибка при удалении оценки \n", e)
        elif choice == '19':
            try:
                course_id = int(input("Номер курса: "))
                q = g.get_by_student_course(course_id)
                for i in q:
                    print(i)
            except Exception as e:
                print("Ошибка при получении оценок по курсу \n", e)
        elif choice == '20':
            try:
                course_id = int(input("Номер курса: "))
                student_id = int(input("ID студента: "))
                print(g.get_avg_by_course_student(student_id, course_id))
            except Exception as e:
                print("Ошибка при получении среднего балла студента по курсу \n", e)
        elif choice == '21':
            try:
                student_id = int(input("ID студента: "))
                q = g.get_avg_by_student(student_id)
                for i in q:
                    print(i)
            except Exception as e:
                print("Ошибка при получении среднего бала по курсу \n", e)
        elif choice == '22':
            try:
                fak = input("Название факультета: ")
                q = g.get_avg_by_fak(fak)
                for i in q:
                    print(i)
            except Exception as e:
                print("Ошибка при получении среднего бала по факультету \n", e)
        elif choice == '23':
            try:
                delete_all(s, t, c, e, g)
                print("База данных удалена")
            except Exception as x:
                print("Ошибка при удалении данных \n", x)
        elif choice == '24':
            print("Программа завершена")
            break
        else:
            print("Неправильный выбор. Пожалуйста, выберите снова.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
