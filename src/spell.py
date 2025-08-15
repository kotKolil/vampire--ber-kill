from .hero import *
from .animation import *

from pyray import *

class AbcSpell:

    def __init__(self,hero:Hero, enemies_list):
        self.mana_count = 0
        self.description = ""
        self.cooldown = 0
        self.icon = 0
        self.name = 0
        self.icon = None
        self.hero = hero
        self.enemies = enemies_list
        self.animation = None
        self.long_script_start = 0
        self.long_script_time = 0
        self.animation = None

    def __str__(self):
        return self.description

    def script(self):
        pass

    def long_script(self):
        pass

    def play_animation(self):
        pass

class HealthSpell(AbcSpell):

    def __init__(self,hero:Hero, enemies_list):
        super().__init__(hero, enemies_list)
        self.mana_count = 13
        self.description = "Heals 10hp.Takes 13 mana"
        self.icon = load_texture_from_image(load_image("resources/spells_icons/health_spell_icon.png"))
        self.cooldown = 1
        self.name = "heal spell"
        self.long_script_time = 0


    def script(self):
        if self.hero.health != self.hero.base_hp:
            if self.hero.health + 10 <= self.hero.base_hp:
                self.hero.health += 10
            else:
                self.hero.health += self.hero.base_hp - self.hero.health
    def play_animation(self, fps):
        pass

class ShieldSpell(AbcSpell):
    def __init__(self, hero, enemies_list):
        super().__init__(hero, enemies_list)
        self.mana_count = 20
        self.description = "creates magic shield against damage"
        self.icon = load_texture_from_image(load_image("resources/spells_icons/shield_spell_icon.png"))
        self.cooldown = 6
        self.name = "shield spell"
        self.long_script_time = 7
        self.animation = Animation("resources/spell_effects/shield_spell", 1)

    def long_script(self):
        self.hero.health = self.hero.health +  self.hero.health + (self.hero.base_hp - self.hero.health) if \
            self.hero.health < self.hero.base_hp else self.hero.health

    def spell_animation(self, fps):
        draw_texture(self.animation.get_current_frame(fps),
                     floor(self.hero.player_pos_x),
                     floor(self.hero.player_pos_y),
                     WHITE)