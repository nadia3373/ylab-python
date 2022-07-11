"""
Напишите функцию-декоратор, которая сохранит (закэширует) значение
декорируемой функции multiplier (Чистая функция). Если декорируемая функция
будет вызвана повторно с теми же параметрами — декоратор должен вернуть
сохранённый результат, не выполняя функцию.
В качестве структуры для кэша, можете использовать словарь в Python.
*В качестве задания со звездочкой можете использовать
вместо Python-словаря => Redis.
"""

import redis


# Соединение с БД
storage = redis.Redis(host="redis-16878.c8.us-east-1-2.ec2.cloud.redislabs.com",
                      port=16878, password="jgnCd3lntIlFTWhCy98bvShp1f2Vqjqu")


def cache_value(func):
    def wrapper(number):
        # Проверить, есть ли в БД ключ, соответствующий введённому числу.
        # Если есть, получить его.
        if storage.exists(number):
            result = int(storage.get(number))
            print("Значение из базы: " + str(result))
        # При отсутствии в БД этого ключа вызвать функцию multiplier
        # и записать ключ с полученным значением в БД.
        else:
            result = func(number)
            storage.set(number, result)
            print("В базу записано значение: " + str(result))
    return wrapper


@cache_value
def multiplier(number: int):
    return number * 2

if __name__ == "__main__":
    while True:
        n = input("Введите значение: ")
        if n.isdigit():
            n = int(n)
            break
    multiplier(n)
