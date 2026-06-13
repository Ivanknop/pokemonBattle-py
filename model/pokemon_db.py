import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

model_path = os.path.dirname(os.path.realpath(__file__))
api_path = os.path.dirname(model_path)
database_path = os.path.join(api_path, "files", "pokemon.db")


class PokemonDB(db.Model):
    __tablename__ = "pokemon"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    type1 = db.Column(db.String, nullable=False)
    type2 = db.Column(db.String, nullable=True)
    attack = db.Column(db.Float, nullable=False)
    defense = db.Column(db.Float, nullable=False)
    sp_attack = db.Column(db.Float, nullable=False)
    sp_defense = db.Column(db.Float, nullable=False)
    speed = db.Column(db.Float, nullable=False)
    hp = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

    def get_name(self):
        return self.name

    def get_principalType(self):
        return self.type1

    def get_secondaryType(self):
        return self.type2

    def get_attack(self):
        return self.attack

    def get_speed(self):
        return self.speed

    def get_defense(self):
        return self.defense

    def get_sp_attack(self):
        return self.sp_attack

    def get_sp_defense(self):
        return self.sp_defense

    def get_vitality(self):
        return self.hp
    def get_total(self):
        return self.total

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type1": self.type1,
            "type2": self.type2,
            "attack": self.attack,
            "defense": self.defense,
            "sp_attack": self.sp_attack,
            "sp_defense": self.sp_defense,
            "speed": self.speed,
            "hp": self.hp,
            "total": self.total
        }

    def __repr__(self):
        return f"<Pokemon {self.name}>"