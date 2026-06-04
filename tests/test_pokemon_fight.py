class FixedRandom:
    def __init__(self, values):
        self.values = list(values)

    def randrange(self, start, stop=None):
        return self.values.pop(0)

    def random(self):
        return 0.5

def test_fight(charmander):
    from model.pokemon_fight import PokemonFight
    from model.pokemon import Pokemon
    from model.pokemon_combat_rules import PokemonCombatRules
    from model.type_chart import TypeChart, TYPE_CHART
    pokemon_characteristics = {
        "type1": "normal",
        "type2": "",
        "attack": 1000,
        "defense": 1000,
        "sp_attack": 1000,
        "sp_defense": 1000, 
        "speed": 1000,
        "total": 5000
    }        
    pokemon = Pokemon("Testmon",1000, pokemon_characteristics)
    assert charmander.name =='Charmander'
    
    fixed_rng = FixedRandom([
        0,   # iniciativa Testmon
        0,   # iniciativa Charmander
        50,  # tirada de suerte
    ])
    
    combat_rules = PokemonCombatRules(TypeChart(TYPE_CHART))
    battle = PokemonFight(pokemon, charmander,  rng=fixed_rng)
    assert battle.get_fighter_one().name == 'Testmon'
    assert battle.get_fighter_two().name == 'Charmander'

    assert combat_rules.calculate_base_damage(pokemon,charmander) == 954.9
    assert combat_rules.calculate_base_damage(charmander,pokemon) == 1
    
    result = battle.play_turn()
    assert len(result) > 0
    assert battle.winner().name == "Testmon"
    assert charmander.get_hp() == 0


def test_play_turn_allows_both_pokemon_to_attack(charmander, squirtle):
    from model.pokemon_fight import PokemonFight

    battle = PokemonFight(charmander, squirtle)

    initial_charmander_hp = charmander.get_hp()
    initial_squirtle_hp = squirtle.get_hp()

    events = battle.play_turn(player_luck=0, opponent_luck=0)

    assert len(events) == 2
    assert (
        charmander.get_hp() < initial_charmander_hp
        or squirtle.get_hp() < initial_squirtle_hp
    )


def test_second_pokemon_does_not_attack_if_defeated(charmander):
    from model.pokemon_fight import PokemonFight
    from model.pokemon import Pokemon

    pokemon_characteristics = {
        "type1": "normal",
        "type2": "",
        "attack": 1000,
        "defense": 1000,
        "sp_attack": 1000,
        "sp_defense": 1000,
        "speed": 1000,
        "total": 5000
    }
    testmon = Pokemon("Testmon", 1000, pokemon_characteristics)

    battle = PokemonFight(testmon, charmander)

    events = battle.play_turn(player_luck=0, opponent_luck=0)

    assert len(events) == 1
    assert charmander.is_alive() is False
    assert battle.winner().get_name() == "Testmon"