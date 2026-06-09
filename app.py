import traceback
from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import model.handler_db as handler_db
from model.pokemon_fight import PokemonFight
from model.pokemon import Pokemon
from model.model import db, database_path
from model.pokemon_combat_rules import PokemonCombatRules
from model.type_chart import TypeChart, TYPE_CHART
import random

def pokemon_to_session(pokemon):
    return {
        "name": pokemon.get_name(),
        "type1": pokemon.type1,
        "type2": pokemon.type2,
        "attack": pokemon.attack,
        "defense": pokemon.defense,
        "sp_attack": pokemon.sp_attack,
        "sp_defense": pokemon.sp_defense,
        "speed": pokemon.speed,
        "hp": pokemon.get_hp(),
        "total": pokemon.total,
    }


def pokemon_from_session(data):
    characteristics = {
        "type1": data["type1"],
        "type2": data["type2"],
        "attack": data["attack"],
        "defense": data["defense"],
        "sp_attack": data["sp_attack"],
        "sp_defense": data["sp_defense"],
        "speed": data["speed"],
        "total": data["total"],
    }
    return Pokemon(data["name"], data["hp"], characteristics)


def convert_Pokemon_from_db(a_pokemon_db):
    pokemon_chars = {
        "type1": a_pokemon_db.get_principalType(),
        "type2": a_pokemon_db.get_secondaryType(),
        "attack": a_pokemon_db.get_attack(),
        "defense": a_pokemon_db.get_defense(),
        "sp_attack": a_pokemon_db.get_sp_attack(),
        "sp_defense": a_pokemon_db.get_sp_defense(),
        "speed": a_pokemon_db.get_speed(),
    }
    pokemon = Pokemon(a_pokemon_db.get_name(), a_pokemon_db.get_hp(), pokemon_chars)
    return pokemon

def create_app():
    app = Flask(__name__)
    app.secret_key ="pokemon-secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    @app.route('/')
    def index():
        return render_template('index.html')

    # Ruta que se ingresa por la ULR 127.0.0.1:5000
    @app.route("/characters")
    def characters():
        try:
            # Obtener de la query string los valores de limit y offset
            limit_str = str(request.args.get('limit'))
            offset_str = str(request.args.get('offset'))
            limit = 0
            offset = 0
            if(limit_str is not None) and (limit_str.isdigit()):
                limit = int(limit_str)
            if(offset_str is not None) and (offset_str.isdigit()):
                offset = int(offset_str)
            data = handler_db.show(limit=limit, offset=offset)
            return render_template('table.html', data=data)
        except Exception:
            return jsonify({"trace": traceback.format_exc()}), 500       

    @app.route("/choose_character")
    def choose_character():
        try:
            limit_str = str(request.args.get("limit"))
            offset_str = str(request.args.get("offset"))
            limit = 0
            offset = 0

            if limit_str is not None and limit_str.isdigit():
                limit = int(limit_str)

            if offset_str is not None and offset_str.isdigit():
                offset = int(offset_str)

            data = handler_db.show(limit=limit, offset=offset)
            random.shuffle(data)
            return render_template("choose_character.html", pokemon_db=data)

        except Exception:
            return jsonify({"trace": traceback.format_exc()}), 500
        
    @app.route("/start_fight", methods=["GET"])
    def start_fight():
        try:
            name_character = request.args.get("jugador")

            pokemon_db = handler_db.find_pokemon(name_character)
            opponent_db = handler_db.random_pokemon_excluding(name_character)

            a_pokemon = convert_Pokemon_from_db(pokemon_db)
            opponent = convert_Pokemon_from_db(opponent_db)

            session["fighter_one"] = pokemon_to_session(a_pokemon)
            session["fighter_two"] = pokemon_to_session(opponent)
            session["events"] = []
            session["finished"] = False
            session["winner"] = None
            session["winner_role"] = None
            session["player_luck"] = 0
            session["opponent_luck"] = 0
            session["pending_player_luck"] = None
            session["pending_opponent_luck"] = None
            session["luck_used_this_turn"] = False
            return redirect(url_for("fight_screen"))

        except Exception:
            return jsonify({"trace": traceback.format_exc()}), 500

    @app.route("/fight", methods=["GET"])
    def fight_screen():
        try:
            fighter_one = session.get("fighter_one")
            fighter_two = session.get("fighter_two")
            events = session.get("events", [])
            finished = session.get("finished", False)
            winner = session.get("winner")
            winner_role = session.get("winner_role")

            if fighter_one is None or fighter_two is None:
                return redirect(url_for("choose_character"))
            return render_template(
                "fight.html",
                fighter_one=fighter_one,
                fighter_two=fighter_two,
                events=events,
                finished=finished,
                winner=winner,
                winner_role=winner_role,
                player_luck=session.get("player_luck", 0),
                opponent_luck=session.get("opponent_luck", 0),
                pending_player_luck=session.get("pending_player_luck"),
                pending_opponent_luck=session.get("pending_opponent_luck"),
                luck_used_this_turn=session.get("luck_used_this_turn", False),
            )

        except Exception:
            return jsonify({"trace": traceback.format_exc()}), 500
        
    @app.route("/fight/next", methods=["POST"])
    def next_turn():
        try:
            fighter_one_data = session.get("fighter_one")
            fighter_two_data = session.get("fighter_two")
            if fighter_one_data is None or fighter_two_data is None:
                return redirect(url_for("choose_character"))
            fighter_one = pokemon_from_session(fighter_one_data)
            fighter_two = pokemon_from_session(fighter_two_data)
            battle = PokemonFight(fighter_one, fighter_two)
            player_luck = int(session.get("player_luck", 0))
            opponent_luck = int(session.get("opponent_luck", 0))
            result = battle.play_turn(
                player_luck=player_luck,
                opponent_luck=opponent_luck,
            )
            session["fighter_one"] = pokemon_to_session(fighter_one)
            session["fighter_two"] = pokemon_to_session(fighter_two)
            events = session.get("events", [])
            for event in reversed(result):
                events.insert(0, event)
            session["events"] = events
            winner = battle.winner()
            if winner is not None:
                session["finished"] = True
                session["winner"] = winner.get_name()
                if winner.get_name() == fighter_one.get_name():
                    session["winner_role"] = "Jugador"
                else:
                    session["winner_role"] = "Rival"
            session["player_luck"] = 0
            session["opponent_luck"] = 0
            session["pending_player_luck"] = None
            session["pending_opponent_luck"] = None
            session["luck_used_this_turn"] = False

            return redirect(url_for("fight_screen"))

        except Exception:
            return jsonify({"trace": traceback.format_exc()}), 500
        
    @app.route("/fight/luck", methods=["POST"])
    def roll_luck():
        try:
            combat_rules = PokemonCombatRules(TypeChart(TYPE_CHART))
            luck_pair = combat_rules.roll_luck_pair(random)

            session["pending_player_luck"] = luck_pair["player_luck"]
            session["pending_opponent_luck"] = luck_pair["opponent_luck"]
            session["luck_used_this_turn"] = True
            return redirect(url_for("fight_screen"))

        except Exception:
            return jsonify({"trace": traceback.format_exc()}), 500

    @app.route("/fight/luck/reject", methods=["POST"])
    def reject_luck():
        try:
            session["pending_player_luck"] = None
            session["pending_opponent_luck"] = None
            return redirect(url_for("fight_screen"))

        except Exception:
            return jsonify({"trace": traceback.format_exc()}), 500
    @app.route("/fight/luck/accept", methods=["POST"])
    def accept_luck():
        try:
            session["player_luck"] = session.get("pending_player_luck", 0)
            session["opponent_luck"] = session.get("pending_opponent_luck", 0)

            session["pending_player_luck"] = None
            session["pending_opponent_luck"] = None

            return redirect(url_for("fight_screen"))

        except Exception:
            return jsonify({"trace": traceback.format_exc()}), 500

    @app.route("/type_chart")
    def type_chart():
        try:
            return render_template(
                "type_chart.html",
                type_chart=TYPE_CHART,
                types=sorted(TYPE_CHART.keys()),
            )

        except Exception:
            return jsonify({"trace": traceback.format_exc()}), 500

    return app
app = create_app()


if __name__ == "__main__":
    app.run(debug=True)