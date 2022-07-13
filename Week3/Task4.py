from itertools import cycle


class CyclicIterator:
    def __init__(self, container):
        # Убедиться, что объект является итерируемым.
        if hasattr(container, '__iter__'):
            self.container = cycle(container)
        else:
            print("Объект не является итерируемым.")
            exit()

    def __iter__(self):
        return self

    def __next__(self):
        # Вернуть следующий элемент.
        for item in self.container:
            return item

cyclic_iterator = CyclicIterator(range(3))
for i in cyclic_iterator:
    # Убедиться, что объект не пуст.
    if i is None:
        print("Итерируемый объект пуст.")
        break
    else:
        print(i)
