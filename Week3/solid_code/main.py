from typing import Union
from heroes import Superman, ChuckNorris, SuperHero
from places import Kostroma, Tokyo, Krypton
from massmedia import TV, Newspapers, CrossPlanetMedia


def save_the_place(hero: SuperHero, place: Union[Kostroma, Tokyo]):
    hero.find(place)
    hero.attack()
    if hero.can_use_ultimate_attack:
        hero.ultimate()
    """
    Добавить оповещение о победе героя на ТВ и в газетах.
    Также оповещается планета Криптон.
    """
    TV(hero, place).create_news()
    Newspapers(hero, place).create_news()
    CrossPlanetMedia(hero, place, Krypton()).cross_planet_signal()

if __name__ == "__main__":
    save_the_place(Superman(), Kostroma())
    print("-" * 20)
    save_the_place(ChuckNorris(), Tokyo())
