from .hero import *
from pyray import *

class AbcSpell:

    def __init__(self, icon_path, hero:Hero, enemies_list):
        self.mana_count = 0
        self.description = ""
        self.cooldown = 0
        self.icon = 0
        self.name = 0
        self.icon = load_texture_from_image(load_image(icon_path))
        self.hero = hero
        self.enemies = enemies_list

    def __str__(self):
        return self.description

    def script(self):
        pass

class HealthSpell(AbcSpell):

    def __init__(self, icon_path, hero:Hero, enemies_list):
        super().__init__(icon_path, hero, enemies_list)
        self.mana_count = 13
        self.description = "Heals 10hp.Takes 13 mana"
        self.cooldown = 1
        self.name = "heal spell"


    def script(self):
        if self.hero.mana - self.mana_count >= 0 and self.hero.health != self.hero.base_hp:
            if self.hero.health + 10 <= self.hero.base_hp:
                self.hero.health += 10
                self.hero.mana -= self.mana_count
            else:
                self.hero.health += self.hero.base_hp - self.hero.health
                self.hero.mana -= self.mana_count

