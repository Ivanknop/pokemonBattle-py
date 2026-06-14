from model.pokemon_db import db, PokemonDB
from model.pokemon import Pokemon
import random

def insert_entity(name, type1, type2, attack, defense, sp_attack, sp_defense, speed, hp,total):
    a_pokemon = PokemonDB(
        name=name,
        type1=type1,
        type2=type2,
        attack=float(attack),
        defense=float(defense),
        sp_attack=float(sp_attack),
        sp_defense=float(sp_defense),
        speed=float(speed),
        hp=float(hp),
        total=float(total)
    )
    db.session.add(a_pokemon)
    db.session.commit()

    return a_pokemon

def show_entities(limit=0, offset=0):
    query = PokemonDB.query.order_by(PokemonDB.name.asc())
    if limit > 0:
        query = query.limit(limit)
        if offset > 0:
            query = query.offset(offset)
    return [_to_domain(p) for p in query.all()]

def find_entity(name) -> Pokemon:
    pokemon_db = PokemonDB.query.filter(PokemonDB.name == name).first()
    return _to_domain(pokemon_db)

def _to_domain(pokemon_db):
    characteristics = {
        "type1": pokemon_db.get_principalType(),
        "type2": pokemon_db.get_secondaryType(),
        "attack": pokemon_db.get_attack(),
        "defense": pokemon_db.get_defense(),
        "sp_attack": pokemon_db.get_sp_attack(),
        "sp_defense": pokemon_db.get_sp_defense(),
        "speed": pokemon_db.get_speed(),
        "total": pokemon_db.get_total(),
    }
    return Pokemon(pokemon_db.get_name(), pokemon_db.get_vitality(), characteristics)

def delete_entity(name):
    pokemon_db = PokemonDB.query.filter(PokemonDB.name == name).first()
    if pokemon_db is None:
        return False
    db.session.delete(pokemon_db)
    db.session.commit()

    return True

def random_entity_excluding(name):
    pokemons = PokemonDB.query.filter(PokemonDB.name != name).all()
    if len(pokemons) == 0:
        return None
    return _to_domain(random.choice(pokemons))