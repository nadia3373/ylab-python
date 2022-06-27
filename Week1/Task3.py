"""
Написать метод zeros, который принимает на вход целое число (integer)
и возвращает количество конечных нулей в факториале (N! = 1 * 2 * 3 * ... * N) заданного числа
"""

def main():
    # Для проверки
    assert zeros(0) == 0
    assert zeros(6) == 1
    assert zeros(30) == 7

    # Запрашивать ввод у пользователя до тех пор, пока не будет введено число
    while True:
        number = input()
        try:
            number = int(number)
            break
        except:
            print("Must provide an integer")

    # Когда ввод корректен, вызвать функцию подсчёта нулей
    number = zeros(number)
    print(number)


def zeros(n):
    result = 0
    # Деление n на 5 пока n >= 5
    # Сумма остатков от деления = количеству конечных нулей в факториале
    while n >= 5:
        n //= 5
        result += n
    return result

if __name__ == "__main__":
    main()
