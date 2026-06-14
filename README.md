Turn-based Pokémon battle simulator. Web interface built with Flask. Extends [battle-core](https://github.com/Ivanknop/battle-core) and uses [battle-flask](https://github.com/Ivanknop/battle-flask) for shared route handling.

## Dependencies

- Python 3.12+
- [battle-core](https://github.com/Ivanknop/battle-core)
- [battle-flask](https://github.com/Ivanknop/battle-flask)
- Flask, SQLAlchemy

## Setup

```bash
git clone https://github.com/Ivanknop/pokemonBattle-py.git
cd pokemonBattle-py
python -m venv env
source env/bin/activate
pip install -r requirements.txt
pip install git+https://github.com/Ivanknop/battle-core.git
pip install git+https://github.com/Ivanknop/battle-flask.git
```

Initialize the database:

```bash
cd api
python model/init_db.py
```

Run:

```bash
python -m flask run
```

## Architecture

```
api/
  app.py                        # Flask app factory — project-specific routes only
  model/
    pokemon.py                  # Entity subclass — offensive_power, defensive_power, initiative, from_dict
    pokemon_combat_rules.py     # CombatRules subclass — adds TypeChart multipliers
    pokemon_fight.py            # Fight subclass — implements turn_text
    pokemon_db.py               # SQLAlchemy model (PokemonDB)
    handler_data.py             # DB access — exposes find_entity, random_entity_excluding
    init_db.py                  # Loads CSV data into SQLite
    type_chart.py               # Type effectiveness matrix
```

## Domain-specific extensions

**`PokemonCombatRules`** extends `CombatRules` with type effectiveness. Damage is multiplied by a factor from `TypeChart` based on attacker's primary type vs defender's types.

**`Pokemon.offensive_power()`**: `attack × 0.6 + sp_attack × 0.4`

**`Pokemon.defensive_power()`**: `defense × 0.7 + sp_defense × 0.3`

**`Pokemon.initiative()`**: `speed`

## Running tests

```bash
pytest tests/
```

---