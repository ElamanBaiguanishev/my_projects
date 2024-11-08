import random

print('Добро пожаловать в числовую угадайку')


def max_range():
    while True:
        n = input('\nМаксимальное число? ')
        if not n.isdigit() or int(n) < 1:
            print('Введите целое число больше нуля!')
            continue
        return int(n)


q = max_range()

def get_num():
    while True:
        num = input(f'Введите число от 1 до {q}: ')
        if not num.isdigit() or not (1 <= int(num) <= q):
            print(f'А может быть все-таки введем целое число от 1 до {q}?')
            continue
        return int(num)


secret = random.randint(1, q)


def game():
    x, total = 0, 1
    while x != secret:
        x = get_num()
        if x > secret:
            print('Ваше число больше загаданного, попробуйте еще раз')
            total += 1
            continue
        elif x < secret:
            print('Ваше число меньше загаданного, попробуйте еще раз')
            total += 1
            continue
    print('Вы угадали, поздравляем!')
    print('Количество попыток: ' + str(total))


while True:
    game()
    print('Отличная игра, еще раз?')
    ans = input('Да(Д) или Yes(Y) если желаете продолжить: ')
    if ans.lower() in ('д', 'да', 'yes', 'y'):
        q = max_range()
        secret = random.randint(1, q)
        continue
    else:
        break

print('Спасибо, что играли в числовую угадайку. Еще увидимся...')