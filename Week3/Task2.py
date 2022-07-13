"""
Надо написать декоратор для повторного выполнения декорируемой функции
через некоторое время. Использует наивный экспоненциальный рост времени
повтора (factor) до граничного времени ожидания (border_sleep_time).
"""


import time


def decorator(call_count, start_sleep_time, factor, border_sleep_time):
    def delay_function(func):
        def wrapper(number):
            print(call_count)
            count = 1
            sleep_time = start_sleep_time
            while count <= call_count:
                # Расчёт времени ожидания для текущей итерации.
                if count > 1:
                    if sleep_time < border_sleep_time:
                        sleep_time = sleep_time * 2 ** factor
                    if sleep_time >= border_sleep_time:
                        sleep_time = border_sleep_time
                else:
                    print("Кол-во запусков = " + str(call_count))
                    print("Начало работы")
                # Ожидание.
                time.sleep(sleep_time)
                # Вызов декорируемой функции.
                result = func(number)
                # Печать результата.
                print("Запуск номер " + str(count) + ". Ожидание: " +
                      str(sleep_time) + " секунд. Результат декорируемой "
                      "функции = " + str(result))
                count += 1
            print("Конец работы")
        return wrapper
    return delay_function


@decorator(call_count=10, start_sleep_time=0.01, factor=1, border_sleep_time=2)
def multiplier(number: int):
    return number * 2

if __name__ == "__main__":
    multiplier(2)
