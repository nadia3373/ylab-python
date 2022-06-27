"""
Написать метод count_find_num, который принимает на вход список простых
множителей (primesL) и целое число, предел (limit), после чего попробуйте
сгенерировать по порядку все числа, меньшие значения предела,
которые имеют все и только простые множители простых чисел primesL.
"""
import itertools


def main():
    # Для проверки
    primesL = [2, 3]
    limit = 200
    assert count_find_num(primesL, limit) == [13, 192]

    primesL = [2, 5]
    limit = 200
    assert count_find_num(primesL, limit) == [8, 200]

    primesL = [2, 3, 5]
    limit = 500
    assert count_find_num(primesL, limit) == [12, 480]

    primesL = [2, 3, 5]
    limit = 1000
    assert count_find_num(primesL, limit) == [19, 960]

    primesL = [2, 3, 47]
    limit = 200
    assert count_find_num(primesL, limit) == []

    # Получение ввода от пользователя
    primesL = input("primesL = ")
    # Удаление нечисловых символов
    if primesL.find(",") or primesL.find(", "):
        primesL = primesL.split(",")
    elif primesL.find(" "):
        primesL = primesL.split(" ")
    temp = []
    for i in range(len(primesL)):
        number = ""
        for j in range(len(primesL[i])):
            if primesL[i][j].isdigit():
                number += str(primesL[i][j])
        temp.append(number)
    # Выдать ошибку, если хотя бы одно из значений нечисловое
    if not temp:
        print("Factors must be integers")
    else:
        primesL = temp
    # Проверка, что лимит является числовым значением
    limit = input("limit = ")
    try:
        limit = int(limit)
    except:
        print("Limit must be an integer")
        exit()
    # Вызов функции подсчёта чисел для введённых множителей
    output = count_find_num(primesL, limit)
    # Печать результата
    print(output)


def count_find_num(primesL, limit):
    output = []
    factors = {}
    temp_factors = []
    primesL = set(sorted(primesL, reverse=True))
    # Для каждого множителя определить максимальную степень,
    # в которую его можно возвести, не превысив лимита
    for i in primesL:
        lim = int(limit)
        min_factor = int(i)
        for j in primesL:
            if not j == i:
                lim = int(lim) / int(j)
        while int(min_factor) <= int(lim):
            temp_factors.append(min_factor)
            min_factor *= int(i)
        factors[i] = temp_factors
        temp_factors = []
    # Определение самого длинного набора чисел
    for i in factors:
        max_power = len(factors[i])
        for j in factors:
            if len(factors[j]) > max_power:
                max_power = len(factors[j])
        if max_power == len(factors[i]):
            break
    # Генерация пар множителей в пределах найденных степеней
    combos = list(itertools.product(*factors.values()))
    sums = set()
    # Перемножение пар множителей и фильтрация результатов, превышающих лимит
    for i in range(len(combos)):
        product = 0
        for j in range(len(combos[i])):
            if product == 0:
                product = combos[i][j]
            else:
                product *= combos[i][j]
        if product <= limit:
            sums.add(product)
    try:
        max_value = max(sums)
    except:
        max_value = 0
    if max_value:
        output.append(len(sums))
        output.append(max_value)
        return output
    else:
        return []

if __name__ == "__main__":
    main()
