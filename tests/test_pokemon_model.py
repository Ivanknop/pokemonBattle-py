def test_pokemon_has_expected_characteristics(pikachu):
    characteristics = pikachu.get_characteristics()

    assert characteristics["name"] == "Pikachu"
    assert characteristics["type1"] == "electric"
    assert characteristics["attack"] == 55
    assert characteristics["defense"] == 40
    assert characteristics["sp_attack"] == 50
    assert characteristics["sp_defense"] == 50
    assert characteristics["speed"] == 90
    assert characteristics["hp"] == 35
    assert characteristics["total"] == 320


def test_pokemon_give_hit_combines_attack_and_special_attack(pikachu):
    assert pikachu.give_hit() == 52.5

def test_pokemon_calculates_total_when_missing():
    from model.pokemon import Pokemon

    pokemon = Pokemon(
        "Testmon",
        "normal",
        "",
        10,
        20,
        30,
        40,
        50,
        60,
        210
    )
    assert pokemon.name == "Testmon"
    assert pokemon.type1 == "normal"
    assert pokemon.attack == 10
    assert pokemon.defense == 20
    assert pokemon.sp_attack == 30
    assert pokemon.sp_defense == 40
    assert pokemon.speed == 50
    assert pokemon.hp == 60