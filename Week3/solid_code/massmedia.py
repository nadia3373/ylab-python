from abc import ABC, abstractmethod


"""
Создать родительский класс масс-медиа с абстрактным методом
создания новостей.
"""


class MassMedia(ABC):
    def __init__(self, hero, place):
        self.place = place
        self.hero = hero

    @abstractmethod
    def create_news(self):
        pass


class TV(MassMedia):
    def create_news(self):
        print(f"TV: Breaking news! {self.hero.name} "
              f"saved {self.place.name}!")


class Newspapers(MassMedia):
    def create_news(self):
        print(f"Newspapers: Breaking news! {self.hero.name} "
              f"saved {self.place.name}!")


# Создать класс для межпланетного оповещения.
class CrossPlanetMedia:
    def __init__(self, hero, place, planet):
        self.place = place
        self.hero = hero
        self.planet = planet

    def cross_planet_signal(self):
        print(f"Planet {self.planet.name} located at "
              f"{self.planet.coordinates[0]}, {self.planet.coordinates[1]} "
              f"was informed that {self.hero.name} saved {self.place.name}!")
