import traceback
from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import model.handler_db as handler_db
from model.pokemon_fight import PokemonFight
from model.pokemon import Pokemon
from model.pokemon_db import db, database_path
from model.pokemon_combat_rules import PokemonCombatRules
from model.type_chart import TypeChart, TYPE_CHART
import random

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
            return render_template("choose_character.html", pokemon_db=data)

        except Exception:
            return jsonify({"trace": traceback.format_exc()}), 500
        
    @app.route("/start_fight", methods=["GET"])
    def start_fight():
        try:
            name_character = request.args.get("jugador")
            a_pokemon = handler_db.find_pokemon(name_character)
            opponent = handler_db.random_pokemon_excluding(name_character)
            session["fighter_one"] = a_pokemon.to_dict()
            session["fighter_two"] = opponent.to_dict()
            session["events"] = []
            session["finished"] = False
            session["winner"] = None
            session["winner_role"] = None
            session["attacker_luck"] = 0
            session["defender_luck"] = 0
            session["pending_attacker_luck"] = None
            session["pending_defender_luck"] = None
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
                attacker_luck=session.get("attacker_luck", 0),
                defender_luck=session.get("defender_luck", 0),
                pending_attacker_luck=session.get("pending_attacker_luck"),
                pending_defender_luck=session.get("pending_defender_luck"),
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
            fighter_one = Pokemon.from_dict(fighter_one_data)
            fighter_two = Pokemon.from_dict(fighter_two_data)
            battle = PokemonFight(fighter_one, fighter_two)
            attacker_luck = int(session.get("attacker_luck", 0))
            defender_luck = int(session.get("defender_luck", 0))
            result = battle.play_turn(
                attacker_luck=attacker_luck,
                defender_luck=defender_luck,
            )
            session["fighter_one"] = fighter_one.to_dict()
            session["fighter_two"] = fighter_two.to_dict()
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
            session["attacker_luck"] = 0
            session["defender_luck"] = 0
            session["pending_attacker_luck"] = None
            session["pending_defender_luck"] = None
            session["luck_used_this_turn"] = False

            return redirect(url_for("fight_screen"))

        except Exception:
            return jsonify({"trace": traceback.format_exc()}), 500
        
    @app.route("/fight/luck", methods=["POST"])
    def roll_luck():
        try:
            combat_rules = PokemonCombatRules(TypeChart(TYPE_CHART))
            luck_pair = combat_rules.roll_luck_pair(random)

            session["pending_attacker_luck"] = luck_pair["attacker_luck"]
            session["pending_defender_luck"] = luck_pair["defender_luck"]
            session["luck_used_this_turn"] = True
            return redirect(url_for("fight_screen"))

        except Exception:
            return jsonify({"trace": traceback.format_exc()}), 500

    @app.route("/fight/luck/reject", methods=["POST"])
    def reject_luck():
        try:
            session["pending_attacker_luck"] = None
            session["pending_defender_luck"] = None
            return redirect(url_for("fight_screen"))

        except Exception:
            return jsonify({"trace": traceback.format_exc()}), 500
    @app.route("/fight/luck/accept", methods=["POST"])
    def accept_luck():
        try:
            session["attacker_luck"] = session.get("pending_attacker_luck", 0)
            session["defender_luck"] = session.get("pending_defender_luck", 0)

            session["pending_attacker_luck"] = None
            session["pending_defender_luck"] = None

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