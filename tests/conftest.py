import pytest
from model.pokemon import Pokemon

@pytest.fixture
def pikachu():
    return Pokemon(
        name="Pikachu",
        type1="electric",
        type2="",
        attack=55,
        defense=40,
        sp_attack=50,
        sp_defense=50,
        speed=90,
        hp=35,
        total=320,
    )

@pytest.fixture
def bulbasaur():
    return Pokemon(
        name="Bulbasaur",
        type1="grass",
        type2="poison",
        attack=49,
        defense=49,
        sp_attack=65,
        sp_defense=65,
        speed=45,
        hp=45,
        total=318,
    )

@pytest.fixture
def charmander():
    return Pokemon(
        name="Charmander",
        type1="fire",
        type2="",
        attack=52,
        defense=43,
        sp_attack=60,
        sp_defense=50,
        speed=65,
        hp=39,
        total=309,
    )

@pytest.fixture
def squirtle():
    return Pokemon(
        name="Squirtle",
        type1="water",
        type2="",
        attack=48,
        defense=65,
        sp_attack=50,
        sp_defense=64,
        speed=43,
        hp=44,
        total=314,
    )