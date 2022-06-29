"""
Надо написать класс CyclicIterator.
Итератор должен итерироваться по итерируемому объекту
(list, tuple, set, range, Range2, и т. д.), и когда достигнет последнего
элемента, начинать сначала.
"""

from itertools import cycle

class CyclicIterator:
    def __init__(self, container):
        self.container = cycle(container)
    def __iter__(self):
        return self
    def __next__(self):
        for item in self.container:
            return item

cyclic_iterator = CyclicIterator(range(3))
for i in cyclic_iterator:
    print(i)
