from model.model import db, Pokemon
import random

def insert_pokemon(name, type1, type2, attack, defense, sp_attack, sp_defense, speed, hp,total):
    a_pokemon = Pokemon(
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

def show(limit=0, offset=0):
    query = Pokemon.query.order_by(Pokemon.name.asc())
    if limit > 0:
        query = query.limit(limit)
        if offset > 0:
            query = query.offset(offset)
    return query.all()


def find_pokemon(name):
    return Pokemon.query.filter(Pokemon.name == name).first()

def delete_pokemon(name):
    pokemon = find_pokemon(name)
    if pokemon is None:
        return False
    db.session.delete(pokemon)
    db.session.commit()

    return True

def random_pokemon_excluding(name):
    pokemons = Pokemon.query.filter(Pokemon.name != name).all()
    if len(pokemons) == 0:
        return None
    return random.choice(pokemons)