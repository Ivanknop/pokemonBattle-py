from battle_core.entity import Entity

class Pokemon(Entity):
    "creat a pokemon"
    def __init__(self, name, vitality, characteristics):
        super().__init__(name, vitality, characteristics)
        self.type1 = characteristics.get("type1")
        self.type2 = characteristics.get("type2")
        
    def offensive_power(self):
        return self.characteristics["attack"] * 0.6 + self.characteristics["sp_attack"] * 0.4

    def defensive_power(self):
        return self.characteristics["defense"] * 0.7 + self.characteristics["sp_defense"] * 0.3

    def initiative(self):
        return self.characteristics["speed"]
    
    def get_principalType(self):
        return self.type1
    
    def get_secondaryType(self):
        return self.type2
    
    def get_hp(self):
        return self.get_vitality()
