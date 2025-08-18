from numpy.ma.core import arcsin

from .hero import *
from .particles import *
from math import *

from pyray import *

class AbcSpell:

    def __init__(self, game_class):
        self.game_class = game_class
        self.mana_count = 0
        self.description = ""
        self.cooldown = 0
        self.icon = 0
        self.name = 0
        self.icon = None
        self.hero = game_class.hero
        self.enemies = game_class.ENEMIES
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

    def spell_animation(self, fps):
        pass

class HealthSpell(AbcSpell):

    def __init__(self, game_class):
        super().__init__(game_class)
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
    def spell_animation(self, fps):
        pass

class ShieldSpell(AbcSpell):
    def __init__(self, games_class):
        super().__init__(games_class)
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

class LightSpheresSpell(AbcSpell):

    def __init__(self, game_class):
        super().__init__(game_class)
        self.mana_count = 15
        self.description = "creates spheres of light against enemies"
        self.icon = load_texture_from_image(load_image("resources/spells_icons/light_wave.png"))
        self.cooldown = 7
        self.name = "light sphere spell"
        self.long_script_time = 0
        self.animation = None

    def script(self):
        self.game_class.PARTICLES +=  [
            DamageSpellParticle(
                cos(i) // abs(cos(i)), sin(i) // abs(sin(i)),
                self.hero.player_pos_x + self.hero.texture.width  * cos(i) // 2,
                self.hero.player_pos_y + self.hero.texture.height  * sin(i) // 2,
                self.game_class.ENEMIES,
                ) for i in range(1, 361, 30)
            ]
