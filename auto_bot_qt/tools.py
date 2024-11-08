from Lesson import lessons
from Users import users


class Data:
    @staticmethod
    def user_input() -> tuple[dict, str]:
        if not users:
            print("Список пользователей пуст")
        try:
            for i, fio in enumerate(users.keys()):
                print(f"{i + 1}. {fio}")
            print("Введите номер студента:")
            num = int(input())
            fio = list(users.keys())[num - 1]
            return users[fio], fio
        except Exception as e:
            print("Ошибка:", e)
            return Data.user_input()

    @staticmethod
    def lesson_input() -> str:
        if not lessons:
            print("Список пользователей пуст")
        try:
            for i, lesson_name in enumerate(lessons.keys()):
                print(f"{i + 1}. {lesson_name}")
            print("Выберите номер предмета")
            num = int(input())
            lesson_name = list(lessons.keys())[num - 1]
            return lessons[lesson_name]
        except Exception as e:
            print("Ошибка:", e)
            return Data.lesson_input()