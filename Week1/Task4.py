"""
Написать метод bananas, который принимает на вход строку и
возвращает количество слов «banana» в строке.
"""

import itertools
import re

source = "banana"
wordmap = {}
sourcemap = {}


def main():
    # Запрос ввода у пользователя
    word = input()
    result = bananas(word)
    # Печать отсортированного результата
    print(set(sorted(result)))


# Функция для разделения слов на буквы и составления буквенной карты
def split_word(s):
    map = {}
    temp = []
    for i in range(len(s)):
        if s[i] not in map:
            letter = s[i]
            temp.append(i)
            j = i + 1
            while j < len(s):
                if s[j] == letter:
                    temp.append(j)
                j += 1
            map[letter] = temp
            temp = []
    return map


def bananas(s) -> set:
    result = set()
    # Составление буквенных карт для искомого и введённого слова
    wordmap = split_word(s)
    sourcemap = split_word(source)
    pattern = "[a-z]?b(-+)?a(-+)?n(-+)?a(-+)?n(-+)?a[a-z]?"
    # Получение всех возможных сочетаний позиций для каждой буквы
    for i in wordmap:
        wordmap[i] = list(itertools.combinations(wordmap[i],
                          len(sourcemap[i])))
    # Получение всех возможных сочетаний букв
    wordmap = list(itertools.product(*wordmap.values()))
    combos = []
    # Запись сочетаний в буквеннов виде
    for i in range(len(wordmap)):
        temp = []
        for j in range(len(source)):
            match = False
            for k in range(len(wordmap[i])):
                for l in range(len(wordmap[i][k])):
                    if ((source[j] == s[wordmap[i][k][l]]) and
                            (not str(wordmap[i][k][l]) in temp)):
                        if len(temp) > 1:
                            if int(temp[len(temp) - 1]) > int(wordmap[i][k][l]):
                                break
                        temp.append(str(wordmap[i][k][l]))
                        match = True
                    if match:
                        break
                if match:
                    break
        if (len(temp) == len(source)):
            combos.append(temp)
    # Фильтрация результатов, не соответствующих искомому слова
    for i in range(len(combos)):
        temp = ""
        for j in range(len(s)):
            if str(j) in combos[i]:
                temp += s[j]
            else:
                temp += "-"
        if re.search(pattern, temp):
            result.add(temp)
    return result

if __name__ == "__main__":
    main()
