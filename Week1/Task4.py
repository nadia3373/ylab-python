"""
Написать метод bananas, который принимает на вход строку и
возвращает количество слов «banana» в строке.
"""

import itertools
import re

WORD = "banana"
DASH = "-"
DASHES_QTY = 0
# Составление шаблона для фильтра результатов по искомому слову
TEMPLATE = "[a-z]?"
for i in range(len(WORD)):
    TEMPLATE += WORD[i]
    if not i == len(WORD) - 1:
        TEMPLATE += "(-+)?"
TEMPLATE += "[a-z]?"


def main():
    # Для проверки
    assert bananas("banann") == set()
    assert bananas("banana") == {"banana"}
    assert bananas("bbananana") == {"b-an--ana", "-banana--", "-b--anana",
                                    "b-a--nana", "-banan--a", "b-ana--na",
                                    "b---anana", "-bana--na", "-ba--nana",
                                    "b-anan--a", "-ban--ana", "b-anana--"}
    assert bananas("bananaaa") == {"banan-a-", "banana--", "banan--a"}
    assert bananas("bananana") == {"ban--ana", "ba--nana", "bana--na",
                                   "b--anana", "banana--", "banan--a"}
    # Запрос ввода у пользователя
    source = input()
    # Вызов функции bananas
    result = bananas(source)
    # Печать отсортированного результата
    for i in sorted(result, reverse=True):
        print(i)


def bananas(s) -> set:
    # Определить количество дефисов для замены лишних букв
    DASHES_QTY = len(s) - len(WORD)
    result = set()
    # Скомбинировать все возможные варианты размещения дефиса в слове
    for i in itertools.product((True, False), repeat=len(s)):
        string = "".join(letter if val else DASH for letter, val in zip(s, i))
        # Отфильтровать только те варианты,
        # из которых можно составить нужное слово
        if re.search(TEMPLATE, string):
            result.add(string)
    delete_items = []
    # Отфильтровать результаты с лишними буквами
    for i in result:
        count = 0
        for j in range(len(i)):
            if i[j] == "-":
                count += 1
        if not count == DASHES_QTY:
            delete_items.append(i)
    # Удалить лишние результаты
    for i in range(len(delete_items)):
        result.remove(delete_items[i])
    # Вернуть результат, либо пустой набор
    if not result:
        return set()
    else:
        return set(result)

if __name__ == "__main__":
    main()
