import os
import csv

from app import create_app
from model.model import db
from model.handler_db import insert_pokemon


script_path = os.path.dirname(os.path.realpath(__file__))
csv_path = os.path.join(script_path, "files/pokemon_estadisticas_pd.csv")


def create_schema():
    db.create_all()


def drop_schema():
    db.drop_all()


def fill():
    with open(csv_path, "r", encoding="utf8") as fi:
        data = list(csv.DictReader(fi))

        for row in data:
            insert_pokemon(
                row["name"],
                row["type1"],
                row["type2"],
                row["attack"],
                row["defense"],
                row["sp_attack"],
                row["sp_defense"],
                row["speed"],
                row["hp"],
                row["total"]
            )


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        drop_schema()
        create_schema()
        fill()

    print("Base de datos creada y cargada correctamente.")