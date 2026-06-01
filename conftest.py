import pytest
from model.pokemon import Pokemon

@pytest.fixture
def pikachu():
    characteristics = {
        "type1": "electric",
        "type2": "",
        "attack": 55,
        "defense": 40,
        "sp_attack": 50,
        "sp_defense": 50,
        "speed": 90,
        "total": 320}
    return Pokemon(name="Pikachu", vitality=35, characteristics=characteristics)

@pytest.fixture
def bulbasaur():
    characteristics = {
        "type1": "grass",
        "type2": "poison",
        "attack": 49,
        "defense": 49,
        "sp_attack": 65,
        "sp_defense": 65,
        "speed": 45,
        "total": 318
    }
    return Pokemon(name="Bulbasaur", vitality=64, characteristics=characteristics)

@pytest.fixture
def charmander():
    characteristics = {
        "type1": "fire",
        "type2": "",
        "attack": 52,
        "defense": 43,
        "sp_attack": 60,
        "sp_defense": 50,
        "speed": 65,
        "total": 309
    }
    return Pokemon(name="Charmander", vitality=39, characteristics=characteristics)

@pytest.fixture
def squirtle():
    characteristics = {
        "type1": "water",
        "type2": "",
        "attack": 48,
        "defense": 65,
        "sp_attack": 50,
        "sp_defense": 64,
        "speed": 43,
        "total": 314
    }
    return Pokemon(name="Squirtle", vitality=44, characteristics=characteristics)