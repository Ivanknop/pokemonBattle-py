import random

from model.type_chart import TypeChart, TYPE_CHART
from model.combat_rules import CombatRules


class Fight:
    def __init__(self, fighter_one, fighter_two, combat_rules=None, rng=None):
        self.__fighter_one = fighter_one
        self.__fighter_two = fighter_two
        self.__rng = rng or random
        self.__combat_rules = combat_rules or CombatRules(TypeChart(TYPE_CHART))

    def get_fighter_one(self):
        return self.__fighter_one

    def get_fighter_two(self):
        return self.__fighter_two

    def get_combat_rules(self):
        return self.__combat_rules

    def order_to_hit(self, player_luck=0, opponent_luck=0):
        fighter_one_initiative = self.__combat_rules.initiative_score(
            self.get_fighter_one(),
            player_luck,
        )
        fighter_two_initiative = self.__combat_rules.initiative_score(
            self.get_fighter_two(),
            opponent_luck,
        )
        if fighter_one_initiative >= fighter_two_initiative:
            return self.get_fighter_one(), self.get_fighter_two()
        return self.get_fighter_two(), self.get_fighter_one()

    def play_turn(self, player_luck=0, opponent_luck=0):
        player_luck = int(player_luck)
        opponent_luck = int(opponent_luck)

        if not self.both_fighters_are_alive():
            winner = self.winner()
            if winner is None:
                return ["La batalla terminó sin vencedor."]
            return ["La batalla ya terminó. Vencedor " + winner.get_name()]

        first_attacker, second_attacker = self.order_to_hit(
            player_luck,
            opponent_luck,
        )
        events = []
        events.append(
            self.attack_once(
                first_attacker,
                second_attacker,
                player_luck,
                opponent_luck,
            )
        )
        if second_attacker.is_alive():
            events.append(
                self.attack_once(
                    second_attacker,
                    first_attacker,
                    player_luck,
                    opponent_luck,
                )
            )

        return events
    
    def both_fighters_are_alive(self):
        return self.get_fighter_two().is_alive() and self.get_fighter_one().is_alive()

    def winner(self):
        if self.__fighter_one.is_alive() and not self.__fighter_two.is_alive():
            return self.__fighter_one
        if self.__fighter_two.is_alive() and not self.__fighter_one.is_alive():
            return self.__fighter_two
        return None
    def attack_once(self, attacker, defender, player_luck, opponent_luck):
        attacker_luck, defender_luck = self.luck_for(
            attacker,
            defender,
            player_luck,
            opponent_luck,
        )
        defender_initial_hp = defender.get_hp()
        damage = self.__combat_rules.calculate_turn_damage(
            attacker,
            defender,
            attacker_luck,
            defender_luck,
        )
        if damage > 0:
            defender.take_hit(damage)
        return self.turn_text(
            attacker,
            defender,
            damage,
            attacker_luck,
            defender_luck,
            defender_initial_hp,
        )
    
    def luck_for(self, attacker, defender, player_luck, opponent_luck):
        if attacker == self.__fighter_one:
            return player_luck, opponent_luck

        return opponent_luck, player_luck
    def turn_text(self, attacker, defender, damage, attacker_luck, defender_luck, defender_initial_hp):
        attacker_name = attacker.get_name()
        defender_name = defender.get_name()

        if self.__combat_rules.is_automatic_failure(attacker_luck):
            return f"{attacker_name} falló"
        if self.__combat_rules.is_blocked(attacker, defender, attacker_luck, defender_luck):
            return (
                f"{defender_name} bloqueó a {attacker_name} y solo recibió {damage} de daño"
            )

        if self.__combat_rules.critical_multiplier(
            attacker,
            defender,
            attacker_luck,
            defender_luck,
        ) > 1:
            return (
                f"{attacker_name} ha dado un crítico dañando por {damage} a {defender_name}"
            )

        if defender_initial_hp <= 0:
            return (
                f"{attacker_name} ha dado un buen golpe por {damage} a {defender_name}"
            )

        damage_ratio = damage / defender_initial_hp

        if damage_ratio > 0.5:
            return f"{attacker_name} dio un duro golpe de {damage} a {defender_name}"

        if damage_ratio < 0.1:
            return (
                f"{attacker_name} golpeó suavemente y solo le hizo {damage} a {defender_name}"
            )

        return f"{attacker_name} ha dado un buen golpe por {damage} a {defender_name}"