def test_pokemon_has_expected_characteristics(pikachu):
    characteristics = pikachu.get_characteristics()

    assert pikachu.get_name() == "Pikachu"
    assert pikachu.get_principalType() == "electric"
    assert characteristics["attack"] == 55
    assert characteristics["defense"] == 40
    assert characteristics["sp_attack"] == 50
    assert characteristics["sp_defense"] == 50
    assert characteristics["speed"] == 90
    assert pikachu.get_hp() == 35
    assert characteristics["total"] == 320


def test_pokemon_offensive_power(pikachu):
    assert pikachu.offensive_power() == 53

def test_pokemon_calculates_total_when_missing():
    from model.pokemon import Pokemon
    pokemon_characteristics = {
        "type1": "normal",
        "type2": "",
        "attack": 10,
        "defense": 20,
        "sp_attack": 30,
        "sp_defense": 40, 
        "speed": 50
    }
    pokemon = Pokemon("Testmon", 1000, pokemon_characteristics)

    assert pokemon.get_name() == "Testmon"
    assert pokemon.get_principalType() == "normal"
    assert pokemon.get_characteristics() == pokemon_characteristics
    assert pokemon.get_characteristics()["attack"] == 10
    assert pokemon.get_characteristics()["defense"] == 20
    assert pokemon.get_characteristics()["sp_attack"] == 30
    assert pokemon.get_characteristics()["sp_defense"] == 40
    assert pokemon.get_characteristics()["speed"] == 50
    assert pokemon.get_hp() == 1000