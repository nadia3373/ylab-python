"""
Написать метод int32_to_ip, который принимает на вход 32-битное целое число
(integer) и возвращает строковое представление его в виде IPv4-адреса
"""

import sys


def main():
    # Запрашивать ввод у пользователя до тех пор, пока не будет введено число
    while True:
        int32 = input()
        try:
            int32 = int(int32)
            break
        except:
            print("Must provide an integer")

    # Для проверки
    assert int32_to_ip(2154959208) == "128.114.17.104"
    assert int32_to_ip(0) == "0.0.0.0"
    assert int32_to_ip(2149583361) == "128.32.10.1"
    # Вызов функции перевода в ip-адрес и вывод результата
    output = int32_to_ip(int32)
    print(output)


def int32_to_ip(int32):
    octets = []
    shift = 24
    reverse = -shift
    for i in range(4):
        # Извлечение значений с помощью битовой маски
        # с учётом прямого или обратного порядка битов
        if sys.byteorder == "little":
            octets.append((int32 >> shift) & 0xff)
        else:
            octets.append((int32 >> (shift + reverse)) & 0xff)
        shift -= 8
        reverse += 16
        # Составление строки ip-адреса
        if i == 0:
            output = str(octets[i])
        else:
            output += "." + str(octets[i])
    return output

if __name__ == "__main__":
    main()
