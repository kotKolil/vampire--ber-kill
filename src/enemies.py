from pyray import *
from time import time
from random import *

class AbcEnemy:
    def __init__(self, pos_x, pos_y):
        self.base_hp = 0
        self.health = 0
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.texture = ""
        self.damage = 0
        self.latest_attack = 0
        self.attack_radius = 0
        self.cooldown = 0
        self.speed = 0

    def ai_script(self, hero_clas):
        pass

class RobotEnemy(AbcEnemy):

    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.base_hp = 50
        self.health = 50
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.texture = load_texture_from_image(load_image("resources/robot_enemy.png"))
        self.damage = 8
        self.attack_radius = 30
        self.cooldown = 0.6
        self.speed = 2

    def ai_script(self, hero_class):
        if (hero_class.player_pos_x - self.attack_radius < self.pos_x < hero_class.player_pos_x + self.attack_radius) and (hero_class.player_pos_y - self.attack_radius < self.pos_y < hero_class.player_pos_y  + self.attack_radius):

                #adds a cooldown to enemy
                if time() - self.latest_attack < self.cooldown:
                    pass
                else:
                    hero_class.health -= self.damage
                    self.latest_attack = time()
                return 1
        y1 = (hero_class.player_pos_y - self.pos_y) // abs(hero_class.player_pos_y - self.pos_y) if \
            (hero_class.player_pos_y - self.pos_y) != 0 else -1
        x1  = (hero_class.player_pos_x - self.pos_x) // abs(hero_class.player_pos_x - self.pos_x) if \
            (hero_class.player_pos_x - self.pos_x) != 0 else -1
        self.pos_x += self.speed * x1
        self.pos_y += self.speed * y1
        return 1
