"""
Надо написать декоратор для повторного выполнения декорируемой функции
через некоторое время. Использует наивный экспоненциальный рост времени
повтора (factor) до граничного времени ожидания (border_sleep_time).

Для запуска программы с другими параметрами:
python3 Task2.py call_count start_sleep_time factor border_sleep_time
"""


import sys
import time


def delay_function(func):
    def wrapper(number, call_count, start_sleep_time,
                factor, border_sleep_time):
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
            print("Запуск номер " + str(count) + ". Ожидание: " + str(sleep_time) +
                  " секунд. Результат декорируемой функции = " + str(result))
            count += 1
        print("Конец работы")
    return wrapper


@delay_function
def multiplier(number: int):
    return number * 2

if __name__ == "__main__":
    # Если при запуске программы были переданы аргументы,
    # попробовать использовать их.
    if len(sys.argv) == 5:
        float_pattern = "\d+.\d+"
        for i in range(1, len(sys.argv)):
            try:
                call_count = int(sys.argv[1])
                start_sleep_time = float(sys.argv[2])
                factor = float(sys.argv[3])
                border_sleep_time = float(sys.argv[4])
            except:
                print("Количество вызовов функции должно быть целым числом. "
                      "Остальные аргументы должны быть целыми или дробными числами.")
                exit()
    # Иначе использовать аргументы по умолчанию.
    elif len(sys.argv) == 1:
        # Начальное время повтора.
        start_sleep_time = 0.01
        # Во сколько раз нужно увеличить время ожидания.
        factor = 1
        # Граничное время ожидания.
        border_sleep_time = 2
        # Число, описывающее кол-во раз запуска функций.
        call_count = 10
    else:
        print("Некорректное количество аргументов.")
        exit()
    n = 2
    multiplier(n, call_count, start_sleep_time, factor, border_sleep_time)
