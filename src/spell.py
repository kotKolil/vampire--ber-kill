from .hero import *

class AbcSpell:

    def __init__(self):
        self.mana_count = 0
        self.description = ""
        self.cooldown = 0
        self.icon = 0
        self.name = 0

    def __str__(self):
        return self.description

    def script(self, enemies_list, hero:Hero):
        pass

class Health_Spell(AbcSpell):

    def __int__(self):
        self.mana_count = 10
        self.description = "Heals 10hp"
        self.cooldown = 1
        self.icon = ""
        self.name = "heal spell"


    def script(self, enemies_list, hero:Hero):
        self.hero.health += 10