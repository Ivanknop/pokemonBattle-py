import traceback
from flask import Flask, jsonify, render_template
from battle_flask.battle_flask import BattleApp
import model.handler_data as handler_data
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
    battleApp = BattleApp(Pokemon,PokemonFight,combat_rules=PokemonCombatRules(TypeChart),choose_route="choose_character",handler=handler_data)
    battleApp.register_routes(app)
    @app.route('/')
    def index():
        return render_template('index.html')

    # Ruta que se ingresa por la ULR 127.0.0.1:5000
    @app.route("/characters")
    def characters():
        try:
            data = handler_data.show_entities()
            return render_template('table.html', data=data)
        except Exception:
            return jsonify({"trace": traceback.format_exc()}), 500       

    @app.route("/choose_character")
    def choose_character():
        try:
            data = handler_data.show_entities()
            return render_template("choose_character.html", pokemon_db=data)

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