from model.type_chart import TypeChart, TYPE_CHART


class CombatRules:
    def __init__(self, type_chart):
        self.type_chart = type_chart

    def calculate_base_damage(self, attacker, defender):
        type_multiplier = self.type_chart.multiplier_for(attacker, defender)

        if type_multiplier == 0:
            return 0

        offensive_power = attacker.attack * 0.6 + attacker.sp_attack * 0.4
        defensive_power = defender.defense * 0.5 + defender.sp_defense * 0.3

        raw_damage = offensive_power - defensive_power

        return max(1, raw_damage * type_multiplier)

    def calculate_turn_damage(self, attacker, defender, attacker_luck, defender_luck):
        if self.is_automatic_failure(attacker_luck):
            return 0

        damage = self.calculate_base_damage(attacker, defender)

        if damage == 0:
            return 0

        if self.is_blocked(attacker, defender, attacker_luck, defender_luck):
            return 1

        damage = damage * self.critical_multiplier(
            attacker,
            defender,
            attacker_luck,
            defender_luck,
        )

        return max(1, round(damage, 2))

    def initiative_score(self, pokemon, pokemon_luck):
        return pokemon.speed + pokemon_luck

    def modified_speed(self, pokemon, pokemon_luck):
        return pokemon.speed + pokemon_luck

    def is_automatic_failure(self, pokemon_luck):
        return pokemon_luck == 1

    def is_automatic_success(self, pokemon_luck):
        return pokemon_luck == 100

    def is_blocked(self, attacker, defender, attacker_luck, defender_luck):
        if self.is_automatic_failure(attacker_luck):
            return False

        if self.is_automatic_success(attacker_luck):
            return False

        attacker_speed = self.modified_speed(attacker, attacker_luck)
        defender_speed = self.modified_speed(defender, defender_luck)

        return defender_speed >= attacker_speed * 2

    def is_critical_hit(self, attacker, defender, attacker_luck, defender_luck):
        if self.is_automatic_failure(attacker_luck):
            return False

        if self.is_automatic_success(attacker_luck):
            return True

        attacker_speed = self.modified_speed(attacker, attacker_luck)
        defender_speed = self.modified_speed(defender, defender_luck)

        return attacker_speed >= defender_speed * 2

    def critical_multiplier(self, attacker, defender, attacker_luck, defender_luck):
        if self.is_automatic_success(attacker_luck):
            return 3

        if self.is_critical_hit(attacker, defender, attacker_luck, defender_luck):
            return 2

        return 1

    def roll_luck_pair(self, rng):
        return {
            "player_luck": rng.randrange(1, 101),
            "opponent_luck": rng.randrange(1, 101),
        }