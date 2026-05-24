import random
class Pokemon:
    "creat a pokemon"
    def __init__(self, name, type1, type2, attack, defense, sp_attack, sp_defense, speed, hp,total):
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.attack = float(attack)
        self.defense = float(defense)
        self.sp_attack = float(sp_attack)
        self.sp_defense = float(sp_defense)
        self.speed = float(speed)
        self.hp = float(hp)
        self.total = float (total)

    def get_name(self):
        return self.name

    def get_characteristics(self):
        return {
            "name": self.name,
            "type1": self.type1,
            "type2": self.type2,
            "attack": self.attack,
            "defense": self.defense,
            "sp_attack": self.sp_attack,
            "sp_defense": self.sp_defense,
            "speed": self.speed,
            "hp": self.hp,
            "total": self.total,
        }

    def get_hp(self):
        return self.hp

    def give_hit(self):
        return (self.attack + self.sp_attack)/2

    def take_hit(self, damage):
        self.hp = max(0, self.hp - float(damage))

    def energy_wins(self, energy): # no creo que sea un método del objeto
        self.hp += (self.hp * energy)/100
    
    def is_alive(self):
        return self.hp > 0

    def __str__(self): 
         return str(self.characteristics)
        
    def bloq_text(self):
        frases = [f'{self.get_name()} no pudo dar el golpe',f'{self.get_name()} erro',f'{self.get_name()} no fue suficientemente veloz',f'Han esquivado a {self.get_name()}']
        return frases[random.randrange(0,len(frases))]

    def hit_text (self, golpe):
       frases = [f'{self.get_name()} produce una herida de {golpe} de vida',f'{self.get_name()} pega fuerte y quita {golpe} de vida',f'El ataque de {self.get_name()} produce {golpe} en su rival',f'Ataque exitoso de {self.get_name()} produciendo un quitando {golpe} de vida']
       return frases[random.randrange(0,len(frases))]
