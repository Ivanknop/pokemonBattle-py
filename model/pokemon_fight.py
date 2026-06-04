from model.type_chart import TypeChart, TYPE_CHART
from model.pokemon_combat_rules import PokemonCombatRules
from battle_core.fight import Fight

class PokemonFight(Fight):
    def __init__(self, fighter_one, fighter_two, rng=None):
        super().__init__(fighter_one, fighter_two, PokemonCombatRules(TypeChart(TYPE_CHART)), rng)
   
    def turn_text(self, attacker, defender, damage, attacker_luck, defender_luck, defender_initial_hp):
        attacker_name = attacker.get_name()
        defender_name = defender.get_name()

        if self.get_combat_rules().is_automatic_failure(attacker_luck):
            return f"{attacker_name} falló"
        if self.get_combat_rules().is_blocked(attacker, defender, attacker_luck, defender_luck):
            return (
                f"{defender_name} bloqueó a {attacker_name} y solo recibió {damage} de daño"
            )

        if self.get_combat_rules().critical_multiplier(
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