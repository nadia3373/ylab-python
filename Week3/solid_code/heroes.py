from abc import ABC, abstractmethod
from antagonistfinder import AntagonistFinder


# Создать отдельные классы для каждого вида оружия.
class Gun:
    def attack(self):
        print('PIU PIU')


class Lasers:
    def ultimate(self):
        print('Wzzzuuuup!')


class RoundhouseKick:
    def attack(self):
        print('Bump')


class Kick:
    def attack(self):
        print("Kick")


class SuperHero(ABC):

    def __init__(self, name, can_use_ultimate_attack=True):
        self.name = name
        self.can_use_ultimate_attack = can_use_ultimate_attack
        self.finder = AntagonistFinder()

    def find(self, place):
        self.finder.get_antagonist(place)

    """
    Для класса СуперГерой создать обязательный абстрактный метод attack(),
    который должен быть реализован у всех наследников, а также
    необязательный метод ultimate(), который может быть не у всех наследников.
    Методы определяются для каждого наследника с помощью классов оружия.
    """

    @abstractmethod
    def attack(self):
        pass

    def ultimate(self):
        pass


class Superman(Kick, Lasers, SuperHero):
    def __init__(self):
        super(Superman, self).__init__("Clark Kent", True)


# Чак Норрис не может пользоваться методом ultimate()
class ChuckNorris(Gun, SuperHero):
    def __init__(self):
        super(ChuckNorris, self).__init__("Chuck Norris", False)
