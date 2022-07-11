from abc import ABC, abstractmethod


"""
Добавить абстрактный класс Place и унаследовать города от него.
Таким образом, реализация метода get_antagonist() становится обязательной.
"""


class Place(ABC):
    @abstractmethod
    def get_antagonist(self):
        pass


class Kostroma(Place):
    name = 'Kostroma'

    def get_orcs(self):
        print('Orcs hid in the forest')

    def get_antagonist(self):
        self.get_orcs()


class Tokyo(Place):
    name = 'Tokyo'

    def get_godzilla(self):
        print('Godzilla stands near a skyscraper')

    def get_antagonist(self):
        self.get_godzilla()


# Планеты для оповещения о победе.
class Planet:
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates


class Earth(Planet):
    def __init__(self):
        super(Earth, self).__init__("Earth", [3.262317, 95.48573])


class Krypton(Planet):
    def __init__(self):
        super(Krypton, self).__init__("Krypton", [36.83254, 1.316243])
